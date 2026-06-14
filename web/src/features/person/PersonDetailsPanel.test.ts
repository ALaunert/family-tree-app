import { render, screen, within } from "@testing-library/vue";
import { describe, expect, test } from "vitest";

import PersonDetailsPanel from "./PersonDetailsPanel.vue";
import type { PersonDto, RelationshipDto } from "../tree/types";

describe("PersonDetailsPanel", () => {
  test("shows relationship context for the selected person", () => {
    const people: PersonDto[] = [
      {
        id: 1,
        fullName: "Ada Example",
        birthDate: "1815-12-10",
        deathDate: "1852-11-27",
        notes: "Tree Root",
      },
      {
        id: 2,
        fullName: "Grace Partner",
        birthDate: null,
        deathDate: null,
        notes: null,
      },
      {
        id: 3,
        fullName: "Ancestor Parent",
        birthDate: null,
        deathDate: null,
        notes: null,
      },
      {
        id: 4,
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
        sourcePersonId: 3,
        targetPersonId: 1,
      },
      {
        id: 12,
        type: "parent_child",
        sourcePersonId: 1,
        targetPersonId: 4,
      },
    ];

    render(PersonDetailsPanel, {
      props: {
        people,
        person: people[0],
        relationships,
      },
    });

    expect(screen.getByRole("heading", { name: "Ada Example" })).toBeInTheDocument();
    expect(screen.getByText("Tree Root")).toBeInTheDocument();
    expect(
      within(screen.getByRole("heading", { name: "Partners" }).closest("section")!)
        .getByText("Grace Partner"),
    ).toBeInTheDocument();
    expect(
      within(screen.getByRole("heading", { name: "Parents" }).closest("section")!)
        .getByText("Ancestor Parent"),
    ).toBeInTheDocument();
    expect(
      within(screen.getByRole("heading", { name: "Children" }).closest("section")!)
        .getByText("Tree Child"),
    ).toBeInTheDocument();
  });
});
