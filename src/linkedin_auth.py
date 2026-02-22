"""
LinkedIn OAuth 2.0 Authentication Manager
Handles token loading and profile URN fetching.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()


class LinkedInAuth:
    BASE_URL = "https://api.linkedin.com/v2"

    def __init__(self):
        self.access_token = os.getenv("LINKEDIN_ACCESS_TOKEN", "")
        self.person_urn = os.getenv("LINKEDIN_PERSON_URN", "")

        if not self.access_token or self.access_token == "your_access_token_here":
            raise ValueError(
                "LINKEDIN_ACCESS_TOKEN not set in .env\n"
                "Follow the README to get your OAuth access token."
            )

    def get_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        }

    def get_profile_urn(self) -> str:
        """
        Returns the person URN from .env if set correctly,
        otherwise auto-fetches from LinkedIn API.
        Tries /v2/userinfo (openid scope) then /v2/me (r_liteprofile scope).
        """
        # If already set correctly in .env, use it directly
        if (self.person_urn
                and self.person_urn != "urn:li:person:YOUR_ID_HERE"
                and "linkedin.com" not in self.person_urn
                and "/" not in self.person_urn
                and self.person_urn.strip()):
            return self.person_urn

        # Try 1: /v2/userinfo — needs openid + profile scope
        resp = requests.get(f"{self.BASE_URL}/userinfo", headers=self.get_headers(), timeout=10)
        if resp.status_code == 200:
            sub = resp.json().get("sub", "")
            urn = f"urn:li:person:{sub}"
            print(f"[Auth] Fetched Person URN (via userinfo): {urn}")
            print(f"[Auth] >>> Add to .env: LINKEDIN_PERSON_URN={urn}")
            return urn

        # Try 2: /v2/me — needs r_liteprofile scope
        resp2 = requests.get(f"{self.BASE_URL}/me", headers=self.get_headers(), timeout=10)
        if resp2.status_code == 200:
            person_id = resp2.json().get("id", "")
            urn = f"urn:li:person:{person_id}"
            print(f"[Auth] Fetched Person URN (via me): {urn}")
            print(f"[Auth] >>> Add to .env: LINKEDIN_PERSON_URN={urn}")
            return urn

        raise RuntimeError(
            "Could not fetch Person URN. Token is missing required scopes.\n\n"
            "FIX: Regenerate your token with these scopes:\n"
            "  openid  profile  w_member_social  email\n\n"
            "Token generator: https://www.linkedin.com/developers/tools/oauth/token-generator\n"
            "Also add product 'Sign In with LinkedIn using OpenID Connect' to your app."
        )

    def verify_token(self) -> bool:
        """Check token validity — tries both userinfo and me endpoints."""
        try:
            # Try openid endpoint first
            resp = requests.get(f"{self.BASE_URL}/userinfo", headers=self.get_headers(), timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                print(f"[Auth] ✅ Token valid. Logged in as: {data.get('name', 'Unknown')}")
                print(f"[Auth] Sub (person ID): {data.get('sub', '')}")
                return True

            # Fallback to /v2/me
            resp2 = requests.get(f"{self.BASE_URL}/me", headers=self.get_headers(), timeout=10)
            if resp2.status_code == 200:
                data = resp2.json()
                name = f"{data.get('localizedFirstName','')} {data.get('localizedLastName','')}".strip()
                print(f"[Auth] ✅ Token valid. Logged in as: {name}")
                print(f"[Auth] LinkedIn ID: {data.get('id', '')}")
                return True

            print(f"[Auth] ❌ Token invalid. Status: {resp.status_code}")
            print(f"[Auth] Response: {resp.text}")
            print("\n>>> FIX: Get a new token from:")
            print("    https://www.linkedin.com/developers/tools/oauth/token-generator")
            print("    Required scopes: openid  profile  w_member_social")
            return False
        except Exception as e:
            print(f"[Auth] Token verification failed: {e}")
            return False


if __name__ == "__main__":
    # Quick test
    auth = LinkedInAuth()
    auth.verify_token()
    urn = auth.get_profile_urn()
    print(f"Person URN: {urn}")
