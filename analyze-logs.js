#!/usr/bin/env node

import {
  S3Client,
  ListObjectsV2Command,
  GetObjectCommand,
} from "@aws-sdk/client-s3";
import dotenv from "dotenv";
import fs from "fs";
import path from "path";

// Load environment variables
dotenv.config();

const AWS_REGION = process.env.AWS_REGION || "us-west-2";
const AWS_S3_BUCKET = process.env.AWS_S3_BUCKET || "digital-diary";
const AWS_ACCESS_KEY_ID = process.env.AWS_ACCESS_KEY_ID;
const AWS_SECRET_ACCESS_KEY = process.env.AWS_SECRET_ACCESS_KEY;

if (!AWS_ACCESS_KEY_ID || !AWS_SECRET_ACCESS_KEY) {
  console.error(
    "Error: Missing AWS credentials. Ensure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set."
  );
  process.exit(1);
}

const s3Client = new S3Client({
  region: AWS_REGION,
  credentials: {
    accessKeyId: AWS_ACCESS_KEY_ID,
    secretAccessKey: AWS_SECRET_ACCESS_KEY,
  },
});

/**
 * List all user folders in the S3 bucket
 */
async function listUsers() {
  const command = new ListObjectsV2Command({
    Bucket: AWS_S3_BUCKET,
    Delimiter: "/",
  });

  const response = await s3Client.send(command);
  const users = (response.CommonPrefixes || []).map((prefix) =>
    prefix.Prefix.replace(/\/$/, "")
  );
  return users;
}

/**
 * List all log files for a user
 */
async function listUserLogs(username) {
  const logsPrefix = `${username}/logs/`;
  const command = new ListObjectsV2Command({
    Bucket: AWS_S3_BUCKET,
    Prefix: logsPrefix,
  });

  const response = await s3Client.send(command);
  const logs = (response.Contents || [])
    .filter((obj) => obj.Key.endsWith(".json"))
    .map((obj) => ({
      key: obj.Key,
      filename: path.basename(obj.Key),
      lastModified: obj.LastModified,
    }));

  return logs;
}

/**
 * Parse log filename to extract timestamp
 * Filename format: YYYYMMDDTHHmmss-[hash].json
 */
function extractTimestamp(filename) {
  const match = filename.match(/^(\d{8}T\d{6})-/);
  if (match) {
    const datetimeStr = match[1];
    // Parse format: 20260418T214617 -> 2026-04-18T21:46:17
    const year = datetimeStr.substring(0, 4);
    const month = datetimeStr.substring(4, 6);
    const day = datetimeStr.substring(6, 8);
    const hour = datetimeStr.substring(9, 11);
    const minute = datetimeStr.substring(11, 13);
    const second = datetimeStr.substring(13, 15);
    
    const isoString = `${year}-${month}-${day}T${hour}:${minute}:${second}Z`;
    return new Date(isoString).getTime();
  }
  return 0;
}

/**
 * Download and parse a log file from S3
 */
async function getLogFile(s3Key) {
  const command = new GetObjectCommand({
    Bucket: AWS_S3_BUCKET,
    Key: s3Key,
  });

  const response = await s3Client.send(command);
  const body = await response.Body.transformToString();
  return JSON.parse(body);
}

/**
 * Count interactions in a log data
 */
function countInteractions(logData) {
  if (Array.isArray(logData)) {
    return logData.length;
  }
  if (logData && typeof logData === "object" && "interactions" in logData) {
    return Array.isArray(logData.interactions) ? logData.interactions.length : 0;
  }
  return 0;
}

/**
 * Main function to analyze all user logs
 */
async function analyzeUserLogs() {
  console.log("Fetching user list from S3...\n");

  const users = await listUsers();
  console.log(`Found ${users.length} users\n`);

  const userStats = [];

  for (const username of users) {
    console.log(`Processing user: ${username}`);

    const logs = await listUserLogs(username);

    if (logs.length === 0) {
      console.log(`  No logs found for ${username}\n`);
      continue;
    }

    // Find the latest log
    const sortedLogs = logs.sort(
      (a, b) => extractTimestamp(b.filename) - extractTimestamp(a.filename)
    );
    const latestLog = sortedLogs[0];
    
    // Extract datetime from filename format: YYYYMMDDTHHmmss-hash.json
    const match = latestLog.filename.match(/^(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2})-/);
    const lastInteractionTime = match 
      ? `${match[1]}-${match[2]}-${match[3]}T${match[4]}:${match[5]}:${match[6]}Z`
      : "Unknown";

    // Count total interactions across all logs
    let totalInteractions = 0;
    for (const log of logs) {
      try {
        const logData = await getLogFile(log.key);
        totalInteractions += countInteractions(logData);
      } catch (error) {
        console.warn(`  Warning: Could not parse ${log.filename}: ${error.message}`);
      }
    }

    userStats.push({
      username,
      lastInteractionTime,
      totalInteractions,
      logCount: logs.length,
    });

    console.log(`  Last interaction: ${lastInteractionTime}`);
    console.log(`  Total interactions: ${totalInteractions}`);
    console.log(`  Log files: ${logs.length}\n`);
  }

  // Print summary
  console.log("\n=== SUMMARY ===\n");
  console.log("Username\t\t\tLast Interaction\t\tTotal Interactions");
  console.log("-".repeat(80));

  userStats.sort((a, b) => b.totalInteractions - a.totalInteractions);

  for (const stat of userStats) {
    const paddedUsername = stat.username.padEnd(20);
    console.log(
      `${paddedUsername}\t${stat.lastInteractionTime}\t${stat.totalInteractions}`
    );
  }

  console.log("\n" + "=".repeat(80));
  console.log(
    `Total users: ${userStats.length}`
  );
  const totalAllInteractions = userStats.reduce(
    (sum, stat) => sum + stat.totalInteractions,
    0
  );
  console.log(`Total interactions (all users): ${totalAllInteractions}`);
}

// Run the analysis
analyzeUserLogs().catch((error) => {
  console.error("Error during analysis:", error);
  process.exit(1);
});
