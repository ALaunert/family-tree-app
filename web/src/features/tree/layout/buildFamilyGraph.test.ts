import { describe, expect, test } from "vitest";

import { buildFamilyGraph } from "./buildFamilyGraph";
import type { PersonDto, RelationshipDto } from "../types";

describe("buildFamilyGraph", () => {
  test("creates a synthetic family-unit node for a partner pair with children", () => {
    const people: PersonDto[] = [
      {
        id: 1,
        fullName: "Ada Example",
        birthDate: null,
        deathDate: null,
        notes: null,
      },
      {
        id: 2,
        fullName: "Grace Example",
        birthDate: null,
        deathDate: null,
        notes: null,
      },
      {
        id: 3,
        fullName: "Tree Child",
        birthDate: null,
        deathDate: null,
        notes: null,
      },
    ];
    const relationships: RelationshipDto[] = [
      {
        id: 10,
        type: "partner",
        sourcePersonId: 1,
        targetPersonId: 2,
      },
      {
        id: 11,
        type: "parent_child",
        sourcePersonId: 1,
        targetPersonId: 3,
      },
      {
        id: 12,
        type: "parent_child",
        sourcePersonId: 2,
        targetPersonId: 3,
      },
    ];

    const graph = buildFamilyGraph(people, relationships);

    expect(graph.nodes.some((node) => node.type === "family-unit")).toBe(true);
    expect(graph.edges).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          source: "person:1",
          target: "family:1-2",
        }),
        expect.objectContaining({
          source: "person:2",
          target: "family:1-2",
        }),
        expect.objectContaining({
          source: "family:1-2",
          target: "person:3",
        }),
      ]),
    );
  });

  test("creates single-parent family-unit nodes for non-partner parents", () => {
    const people: PersonDto[] = [
      {
        id: 1,
        fullName: "Ada Example",
        birthDate: null,
        deathDate: null,
        notes: null,
      },
      {
        id: 2,
        fullName: "Grace Example",
        birthDate: null,
        deathDate: null,
        notes: null,
      },
      {
        id: 3,
        fullName: "Tree Child",
        birthDate: null,
        deathDate: null,
        notes: null,
      },
    ];
    const relationships: RelationshipDto[] = [
      {
        id: 11,
        type: "parent_child",
        sourcePersonId: 1,
        targetPersonId: 3,
      },
      {
        id: 12,
        type: "parent_child",
        sourcePersonId: 2,
        targetPersonId: 3,
      },
    ];

    const graph = buildFamilyGraph(people, relationships);

    expect(graph.nodes).toEqual(
      expect.arrayContaining([
        expect.objectContaining({ id: "family:1", type: "family-unit" }),
        expect.objectContaining({ id: "family:2", type: "family-unit" }),
      ]),
    );
    expect(graph.edges).toEqual(
      expect.arrayContaining([
        expect.objectContaining({ source: "family:1", target: "person:3" }),
        expect.objectContaining({ source: "family:2", target: "person:3" }),
      ]),
    );
  });
});
