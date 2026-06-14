import type { Edge, Node } from "@vue-flow/core";

export interface PersonDto {
  id: number;
  fullName: string;
  birthDate: string | null;
  deathDate: string | null;
  notes: string | null;
}

export type RelationshipType = "parent_child" | "partner";

export interface RelationshipDto {
  id: number;
  type: RelationshipType;
  sourcePersonId: number;
  targetPersonId: number;
}

export interface TreeDto {
  viewerRole: "viewer" | "moderator" | "owner";
  people: PersonDto[];
  relationships: RelationshipDto[];
}

export interface PersonNodeData extends Record<string, unknown> {
  kind: "person";
  person: PersonDto;
}

export interface FamilyUnitNodeData extends Record<string, unknown> {
  kind: "family-unit";
  parentIds: number[];
}

type FamilyGraphNodeEvents = Record<string, (...args: any[]) => any>;

export type FamilyGraphNode =
  | Node<PersonNodeData, FamilyGraphNodeEvents, "person">
  | Node<FamilyUnitNodeData, FamilyGraphNodeEvents, "family-unit">;

export type FamilyGraphEdge = Edge<Record<string, unknown>>;

export interface FamilyGraph {
  nodes: FamilyGraphNode[];
  edges: FamilyGraphEdge[];
}
