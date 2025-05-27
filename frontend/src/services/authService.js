// frontend/src/services/authService.js
import {
  CognitoUserPool,
  CognitoUser,
  AuthenticationDetails,
  CognitoUserAttribute,
} from "amazon-cognito-identity-js";

// Replace with your actual Cognito configuration
const poolData = {
  UserPoolId: "your-user-pool-id", // e.g., 'us-west-2_xxxxxxxxx'
  ClientId: "your-app-client-id", // e.g., 'xxxxxxxxxxxxxxxxxxxxxxxxxx'
};

const userPool = new CognitoUserPool(poolData);

class AuthService {
  // Sign in user
  signIn(email, password) {
    return new Promise((resolve, reject) => {
      const authenticationData = {
        Username: email,
        Password: password,
      };

      const authenticationDetails = new AuthenticationDetails(
        authenticationData
      );

      const userData = {
        Username: email,
        Pool: userPool,
      };

      const cognitoUser = new CognitoUser(userData);

      cognitoUser.authenticateUser(authenticationDetails, {
        onSuccess: (result) => {
          const accessToken = result.getAccessToken().getJwtToken();
          const idToken = result.getIdToken().getJwtToken();
          const refreshToken = result.getRefreshToken().getToken();

          // Store tokens in memory (not localStorage for Electron security)
          this.setTokens({
            accessToken,
            idToken,
            refreshToken,
          });

          resolve({
            success: true,
            user: result.getIdToken().payload,
            tokens: {
              accessToken,
              idToken,
              refreshToken,
            },
          });
        },
        onFailure: (err) => {
          reject({
            success: false,
            error: err.message || err,
          });
        },
        newPasswordRequired: (userAttributes, requiredAttributes) => {
          // Handle new password required scenario
          resolve({
            success: false,
            newPasswordRequired: true,
            cognitoUser,
            userAttributes,
            requiredAttributes,
          });
        },
      });
    });
  }

  // Sign up new user
  signUp(email, password, attributes = {}) {
    return new Promise((resolve, reject) => {
      const attributeList = [];

      // Add email attribute
      attributeList.push(
        new CognitoUserAttribute({
          Name: "email",
          Value: email,
        })
      );

      // Add other attributes
      Object.keys(attributes).forEach((key) => {
        attributeList.push(
          new CognitoUserAttribute({
            Name: key,
            Value: attributes[key],
          })
        );
      });

      userPool.signUp(email, password, attributeList, null, (err, result) => {
        if (err) {
          reject({
            success: false,
            error: err.message || err,
          });
          return;
        }

        resolve({
          success: true,
          user: result.user,
          userSub: result.userSub,
        });
      });
    });
  }

  // Confirm sign up with verification code
  confirmSignUp(email, verificationCode) {
    return new Promise((resolve, reject) => {
      const userData = {
        Username: email,
        Pool: userPool,
      };

      const cognitoUser = new CognitoUser(userData);

      cognitoUser.confirmRegistration(verificationCode, true, (err, result) => {
        if (err) {
          reject({
            success: false,
            error: err.message || err,
          });
          return;
        }

        resolve({
          success: true,
          result,
        });
      });
    });
  }

  // Set new password (for new password required scenario)
  setNewPassword(cognitoUser, newPassword, attributes = {}) {
    return new Promise((resolve, reject) => {
      cognitoUser.completeNewPasswordChallenge(newPassword, attributes, {
        onSuccess: (result) => {
          const accessToken = result.getAccessToken().getJwtToken();
          const idToken = result.getIdToken().getJwtToken();
          const refreshToken = result.getRefreshToken().getToken();

          this.setTokens({
            accessToken,
            idToken,
            refreshToken,
          });

          resolve({
            success: true,
            user: result.getIdToken().payload,
            tokens: {
              accessToken,
              idToken,
              refreshToken,
            },
          });
        },
        onFailure: (err) => {
          reject({
            success: false,
            error: err.message || err,
          });
        },
      });
    });
  }

  // Get current user
  getCurrentUser() {
    return userPool.getCurrentUser();
  }

  // Check if user is authenticated
  isAuthenticated() {
    const cognitoUser = this.getCurrentUser();
    return new Promise((resolve) => {
      if (!cognitoUser) {
        resolve(false);
        return;
      }

      cognitoUser.getSession((err, session) => {
        if (err || !session.isValid()) {
          resolve(false);
          return;
        }
        resolve(true);
      });
    });
  }

  // Get user session
  getSession() {
    const cognitoUser = this.getCurrentUser();
    return new Promise((resolve, reject) => {
      if (!cognitoUser) {
        reject("No user found");
        return;
      }

      cognitoUser.getSession((err, session) => {
        if (err) {
          reject(err);
          return;
        }
        resolve(session);
      });
    });
  }

  // Sign out
  signOut() {
    const cognitoUser = this.getCurrentUser();
    if (cognitoUser) {
      cognitoUser.signOut();
    }
    this.clearTokens();
  }

  // Token management (in-memory for security)
  tokens = null;

  setTokens(tokens) {
    this.tokens = tokens;
  }

  getTokens() {
    return this.tokens;
  }

  clearTokens() {
    this.tokens = null;
  }

  // Refresh tokens
  refreshSession() {
    return new Promise((resolve, reject) => {
      const cognitoUser = this.getCurrentUser();
      if (!cognitoUser) {
        reject("No user found");
        return;
      }

      cognitoUser.getSession((err, session) => {
        if (err) {
          reject(err);
          return;
        }

        if (session.isValid()) {
          resolve(session);
          return;
        }

        const refreshToken = session.getRefreshToken();
        cognitoUser.refreshSession(refreshToken, (err, session) => {
          if (err) {
            reject(err);
            return;
          }

          const accessToken = session.getAccessToken().getJwtToken();
          const idToken = session.getIdToken().getJwtToken();

          this.setTokens({
            ...this.tokens,
            accessToken,
            idToken,
          });

          resolve(session);
        });
      });
    });
  }
}

export default new AuthService();
