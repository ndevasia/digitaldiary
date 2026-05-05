const dotenv = require('dotenv');
const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');
const readline = require('readline');
const { google } = require('googleapis');
const { S3Client, GetObjectCommand } = require('@aws-sdk/client-s3');

dotenv.config();
dotenv.config({ path: path.resolve(__dirname, '../.env') });

const GOOGLE_DRIVE_SCOPES = ['https://www.googleapis.com/auth/drive'];
const GOOGLE_TOKEN_PATH = path.resolve(__dirname, '.gdrive-token.json');
const GOOGLE_DRIVE_PARENT_FOLDER_ID = process.env.GOOGLE_DRIVE_PARENT_FOLDER_ID || null;
const GOOGLE_DOC_SHORTCUT_NAME = process.env.GOOGLE_DOC_SHORTCUT_NAME || 'Submission Doc';
const GOOGLE_DOC_TARGET_ID = process.env.GOOGLE_DOC_TARGET_ID || resolveGoogleDocId(process.env.GOOGLE_DOC_URL || '');

const AWS_REGION = process.env.AWS_REGION || 'us-west-2';
const AWS_S3_BUCKET = process.env.AWS_S3_BUCKET || 'digital-diary';
const AWS_ACCESS_KEY_ID = process.env.AWS_ACCESS_KEY_ID;
const AWS_SECRET_ACCESS_KEY = process.env.AWS_SECRET_ACCESS_KEY;

let s3Client = null;

function initS3Client() {
    if (s3Client) {
        return s3Client;
    }

    if (!AWS_ACCESS_KEY_ID || !AWS_SECRET_ACCESS_KEY) {
        throw new Error('Missing AWS_ACCESS_KEY_ID or AWS_SECRET_ACCESS_KEY in .env');
    }

    s3Client = new S3Client({
        region: AWS_REGION,
        credentials: {
            accessKeyId: AWS_ACCESS_KEY_ID,
            secretAccessKey: AWS_SECRET_ACCESS_KEY,
        },
    });

    return s3Client;
}

async function readUserJson() {
    try {
        const client = initS3Client();
        const command = new GetObjectCommand({
            Bucket: AWS_S3_BUCKET,
            Key: 'user.json',
        });
        const response = await client.send(command);
        const data = await response.Body.transformToString();
        return JSON.parse(data);
    } catch (error) {
        if (error.name === 'NoSuchKey') {
            console.warn('user.json not found in S3');
            return null;
        }
        throw error;
    }
}

async function fetchUserSecret(username) {
    try {
        const userData = await readUserJson();
        if (!userData) {
            throw new Error('Could not read user data from S3');
        }

        const users = userData.users || {};
        const user = users[username];
        if (!user) {
            throw new Error(`User '${username}' not found in user.json`);
        }

        const secret = user.secret;
        if (!secret) {
            throw new Error(`No secret found for user '${username}'`);
        }

        return secret;
    } catch (error) {
        console.error(`Error fetching secret for ${username}:`, error.message);
        throw error;
    }
}

function resolveGoogleDocId(docValue) {
    const value = String(docValue || '').trim();

    if (!value) {
        return null;
    }

    const match = value.match(/\/d\/([a-zA-Z0-9-_]+)/) || value.match(/id=([a-zA-Z0-9-_]+)/);
    return match ? match[1] : value;
}

function sanitizeFolderName(name) {
    return String(name).trim().replace(/[\\/:*?"<>|]+/g, '-');
}

function getBuildArtifacts() {
    const distPath = path.resolve(__dirname, '../dist');
    const files = [
        path.join(distPath, 'Digital Diary-0.0.0-win.zip'),
        path.join(distPath, 'Digital Diary-0.0.0-arm64-win.zip'),
        path.join(distPath, 'Digital Diary-0.0.0-mac.zip'),
        path.join(distPath, 'Digital Diary-0.0.0-arm64-mac.zip'),
    ];

    return files.filter((filePath) => fs.existsSync(filePath));
}

async function getDriveClient() {
    const auth = await authGoogleDrive();
    return google.drive({ version: 'v3', auth });
}

async function getOrCreateUserFolder(drive, username) {
    const folderName = sanitizeFolderName(username);
    const queryParts = [
        `mimeType = 'application/vnd.google-apps.folder'`,
        `name = '${folderName.replace(/'/g, "\\'")}'`,
        'trashed = false',
    ];

    if (GOOGLE_DRIVE_PARENT_FOLDER_ID) {
        queryParts.push(`'${GOOGLE_DRIVE_PARENT_FOLDER_ID}' in parents`);
    }

    const existing = await drive.files.list({
        q: queryParts.join(' and '),
        fields: 'files(id, name)',
        spaces: 'drive',
    });

    if (existing.data.files && existing.data.files.length > 0) {
        return existing.data.files[0].id;
    }

    const metadata = {
        name: folderName,
        mimeType: 'application/vnd.google-apps.folder',
    };

    if (GOOGLE_DRIVE_PARENT_FOLDER_ID) {
        metadata.parents = [GOOGLE_DRIVE_PARENT_FOLDER_ID];
    }

    const created = await drive.files.create({
        requestBody: metadata,
        fields: 'id',
    });

    console.log(`Created Drive folder for ${username}: ${folderName}`);
    return created.data.id;
}

async function ensureFolderSharedWithLink(drive, folderId) {
    const permissions = await drive.permissions.list({
        fileId: folderId,
        fields: 'permissions(id, type, role, allowFileDiscovery)',
        supportsAllDrives: true,
    });

    const alreadyShared = (permissions.data.permissions || []).some((permission) => {
        return permission.type === 'anyone' && permission.role === 'reader';
    });

    if (alreadyShared) {
        return;
    }

    await drive.permissions.create({
        fileId: folderId,
        requestBody: {
            type: 'anyone',
            role: 'reader',
            allowFileDiscovery: false,
        },
        fields: 'id',
        supportsAllDrives: true,
    });

    console.log(`Shared folder ${folderId} with anyone who has the link.`);
}

async function ensureDocShortcutInFolder(drive, folderId) {
    if (!GOOGLE_DOC_TARGET_ID) {
        throw new Error('Missing GOOGLE_DOC_TARGET_ID or GOOGLE_DOC_URL in .env');
    }

    const existingShortcut = await drive.files.list({
        q: [
            `'${folderId}' in parents`,
            `name = '${GOOGLE_DOC_SHORTCUT_NAME.replace(/'/g, "\\'")}'`,
            `mimeType = 'application/vnd.google-apps.shortcut'`,
            'trashed = false',
        ].join(' and '),
        fields: 'files(id)',
        spaces: 'drive',
        supportsAllDrives: true,
    });

    if ((existingShortcut.data.files || []).length > 0) {
        return;
    }

    await drive.files.create({
        requestBody: {
            name: GOOGLE_DOC_SHORTCUT_NAME,
            parents: [folderId],
            mimeType: 'application/vnd.google-apps.shortcut',
            shortcutDetails: {
                targetId: GOOGLE_DOC_TARGET_ID,
                targetMimeType: 'application/vnd.google-apps.document',
            },
        },
        fields: 'id, name',
        supportsAllDrives: true,
    });

    console.log(`Added Google Docs shortcut to folder ${folderId}.`);
}

async function uploadFileToFolder(drive, folderId, filePath) {
    const fileName = path.basename(filePath);
    const mimeType = 'application/zip';

    await drive.files.create({
        requestBody: {
            name: fileName,
            parents: [folderId],
        },
        media: {
            mimeType,
            body: fs.createReadStream(filePath),
        },
        fields: 'id, name',
        supportsAllDrives: true,
    });

    console.log(`Uploaded ${fileName}`);
}

function getFolderLink(folderId) {
    return `https://drive.google.com/drive/folders/${folderId}?usp=sharing`;
}

async function distributeForUser(drive, username) {
    const artifacts = packageAndDistribute(username);
    const folderId = await getOrCreateUserFolder(drive, username);

    await ensureFolderSharedWithLink(drive, folderId);
    await ensureDocShortcutInFolder(drive, folderId);

    for (const artifact of artifacts) {
        await uploadFileToFolder(drive, folderId, artifact);
    }

    return { username, folderId, folderLink: getFolderLink(folderId) };
}

function packageAndDistribute(username) {
    console.log(`Packaging for ${username}...`);
    try {
        execSync('npm run electron:build:all', { stdio: 'inherit' });
        return getBuildArtifacts();
    } catch (error) {
        console.error(`Error packaging for ${username}:`, error);
        return [];
    }
}

async function authGoogleDrive() {
    const clientId = process.env.GOOGLE_DRIVE_CLIENT_ID || process.env.GOOGLE_CLIENT_ID;
    const clientSecret = process.env.GOOGLE_DRIVE_CLIENT_SECRET || process.env.GOOGLE_CLIENT_SECRET;
    const redirectUri = 'http://localhost';

    if (!clientId || !clientSecret) {
        throw new Error('Missing GOOGLE_DRIVE_CLIENT_ID/GOOGLE_DRIVE_CLIENT_SECRET (or GOOGLE_CLIENT_ID/GOOGLE_CLIENT_SECRET) in .env');
    }

    const oauth2Client = new google.auth.OAuth2(clientId, clientSecret, redirectUri);

    if (fs.existsSync(GOOGLE_TOKEN_PATH)) {
        const token = JSON.parse(fs.readFileSync(GOOGLE_TOKEN_PATH, 'utf-8'));
        oauth2Client.setCredentials(token);
        console.log('Google Drive auth loaded from saved token.');
        return oauth2Client;
    }

    const authUrl = oauth2Client.generateAuthUrl({
        access_type: 'offline',
        prompt: 'consent',
        scope: GOOGLE_DRIVE_SCOPES,
    });

    console.log('Authorize this app by visiting this URL:');
    console.log(authUrl);

    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
    });

    const code = await new Promise((resolve) => {
        rl.question('Paste the authorization code here: ', (answer) => {
            resolve(answer);
        });
    });
    rl.close();

    const { tokens } = await oauth2Client.getToken(String(code).trim());
    oauth2Client.setCredentials(tokens);
    fs.writeFileSync(GOOGLE_TOKEN_PATH, JSON.stringify(tokens, null, 2));
    console.log(`Google Drive token saved to ${GOOGLE_TOKEN_PATH}`);

    return oauth2Client;
}

async function main() {
    const auth = await authGoogleDrive();
    const drive = google.drive({ version: 'v3', auth });
    const folderLinks = [];

    if (process.argv.length > 2) {
        const usernames = process.argv.slice(2);
        const initialUsername = process.env.VITE_USERNAME;
        const initialSecret = process.env.VITE_USER_SECRET;

        for (const username of usernames) {
            let userSecret;
            try {
                userSecret = await fetchUserSecret(username);
            } catch (error) {
                console.error(`Skipping user ${username}: ${error.message}`);
                continue;
            }

            const env = fs.readFileSync(path.resolve(__dirname, './.env'), 'utf-8');
            const updatedEnv = env.replace(/VITE_USERNAME=.*/g, `VITE_USERNAME=${username}`)
                                  .replace(/VITE_USER_SECRET=.*/g, `VITE_USER_SECRET=${userSecret}`);
            fs.writeFileSync(path.resolve(__dirname, './.env'), updatedEnv);
            folderLinks.push(await distributeForUser(drive, username));
        }
        const env = fs.readFileSync(path.resolve(__dirname, './.env'), 'utf-8');
        const restoredEnv = env.replace(/VITE_USERNAME=.*/g, `VITE_USERNAME=${initialUsername}`)
                               .replace(/VITE_USER_SECRET=.*/g, `VITE_USER_SECRET=${initialSecret}`);
        fs.writeFileSync(path.resolve(__dirname, './.env'), restoredEnv);
    } else {
        console.log('No username provided, grabbing from .env');
        const username = process.env.VITE_USERNAME;
        if (username) {
            folderLinks.push(await distributeForUser(drive, username));
        } else {
            console.error('No username found in .env');
        }
    }

    if (folderLinks.length > 0) {
        console.log('Distribution links:');
        for (const entry of folderLinks) {
            console.log(`${entry.username}: ${entry.folderLink}`);
        }
    }
}

main().catch((error) => {
    console.error('Distribution failed:', error);
    process.exitCode = 1;
});
