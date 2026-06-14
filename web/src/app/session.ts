import { fetchJson } from "../lib/fetchJson";

export type UserRole = "owner" | "moderator" | "viewer";

export interface SessionUser {
  id: number;
  email: string;
  role: UserRole;
}

interface AuthUserResponse {
  user: SessionUser;
}

let currentUser: SessionUser | null | undefined;

export async function bootstrapSession(): Promise<SessionUser | null> {
  if (currentUser !== undefined) {
    return currentUser;
  }

  try {
    const response = await fetchJson<AuthUserResponse>("/api/v1/auth/me");
    currentUser = response.user;
  } catch (error) {
    currentUser = null;
  }

  return currentUser;
}

export function setCurrentUser(user: SessionUser | null): void {
  currentUser = user;
}
