import type {
  FamilyGraph,
  FamilyGraphEdge,
  FamilyGraphNode,
  PersonDto,
  RelationshipDto,
} from "../types";

function pairKey(firstId: number, secondId: number): string {
  return [firstId, secondId].sort((left, right) => left - right).join("-");
}

function personNodeId(personId: number): string {
  return `person:${personId}`;
}

function familyNodeId(parentIds: number[]): string {
  return `family:${[...parentIds].sort((left, right) => left - right).join("-")}`;
}

export function buildFamilyGraph(
  people: PersonDto[],
  relationships: RelationshipDto[],
): FamilyGraph {
  const nodes: FamilyGraphNode[] = people.map((person) => ({
    id: personNodeId(person.id),
    type: "person",
    position: { x: 0, y: 0 },
    data: {
      kind: "person",
      person,
    },
  }));
  const edges: FamilyGraphEdge[] = [];
  const partnerPairs = new Set(
    relationships
      .filter((relationship) => relationship.type === "partner")
      .map((relationship) =>
        pairKey(relationship.sourcePersonId, relationship.targetPersonId),
      ),
  );
  const parentsByChild = new Map<number, Set<number>>();

  for (const relationship of relationships) {
    if (relationship.type !== "parent_child") {
      continue;
    }

    const parents = parentsByChild.get(relationship.targetPersonId) ?? new Set();
    parents.add(relationship.sourcePersonId);
    parentsByChild.set(relationship.targetPersonId, parents);
  }

  const familyNodes = new Map<string, number[]>();
  const familyChildLinks = new Set<string>();

  for (const [childId, parentSet] of parentsByChild) {
    const parentIds = [...parentSet].sort((left, right) => left - right);
    const groupedParentIds = new Set<number>();
    const familyGroups: number[][] = [];

    for (const parentId of parentIds) {
      if (groupedParentIds.has(parentId)) {
        continue;
      }

      const partnerId = parentIds.find(
        (candidateId) =>
          candidateId !== parentId &&
          !groupedParentIds.has(candidateId) &&
          partnerPairs.has(pairKey(parentId, candidateId)),
      );

      if (partnerId === undefined) {
        familyGroups.push([parentId]);
        groupedParentIds.add(parentId);
        continue;
      }

      familyGroups.push([parentId, partnerId].sort((left, right) => left - right));
      groupedParentIds.add(parentId);
      groupedParentIds.add(partnerId);
    }

    for (const familyParentIds of familyGroups) {
      const familyId = familyNodeId(familyParentIds);
      familyNodes.set(familyId, familyParentIds);
      familyChildLinks.add(`${familyId}->${personNodeId(childId)}`);
    }
  }

  for (const [familyId, parentIds] of familyNodes) {
    nodes.push({
      id: familyId,
      type: "family-unit",
      position: { x: 0, y: 0 },
      data: {
        kind: "family-unit",
        parentIds,
      },
    });

    for (const parentId of parentIds) {
      edges.push({
        id: `${personNodeId(parentId)}->${familyId}`,
        source: personNodeId(parentId),
        target: familyId,
      });
    }
  }

  for (const link of familyChildLinks) {
    const [source, target] = link.split("->");
    edges.push({
      id: link,
      source,
      target,
    });
  }

  return { nodes, edges };
}
