import type { RelationshipType, PersonDto } from "../tree/types";

export interface PersonInput {
  fullName: string;
  birthDate: string | null;
  deathDate: string | null;
  notes: string | null;
}

export interface RelationshipInput {
  relationshipType: RelationshipType;
  sourcePersonId: number;
  targetPersonId: number;
}

async function writeJson<T>(input: RequestInfo | URL, init: RequestInit): Promise<T> {
  const response = await fetch(input, {
    ...init,
    credentials: "include",
    headers: {
      ...(init.body === undefined ? {} : { "Content-Type": "application/json" }),
      ...init.headers,
    },
  });

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

export function createPerson(person: PersonInput): Promise<PersonDto> {
  return writeJson<PersonDto>("/api/v1/people", {
    method: "POST",
    body: JSON.stringify(person),
  });
}

export function updatePerson(personId: number, person: PersonInput): Promise<PersonDto> {
  return writeJson<PersonDto>(`/api/v1/people/${personId}`, {
    method: "PATCH",
    body: JSON.stringify(person),
  });
}

export function createRelationship(
  relationship: RelationshipInput,
): Promise<void> {
  return writeJson<void>("/api/v1/relationships", {
    method: "POST",
    body: JSON.stringify(relationship),
  });
}

export function deleteRelationship(relationshipId: number): Promise<void> {
  return writeJson<void>(`/api/v1/relationships/${relationshipId}`, {
    method: "DELETE",
  });
}
