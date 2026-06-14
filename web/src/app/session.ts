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

interface BootstrapSessionOptions {
  forceRefresh?: boolean;
}

export async function bootstrapSession(
  options: BootstrapSessionOptions = {},
): Promise<SessionUser | null> {
  if (!options.forceRefresh && currentUser !== undefined) {
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

export function resetSessionForTests(): void {
  currentUser = undefined;
}
