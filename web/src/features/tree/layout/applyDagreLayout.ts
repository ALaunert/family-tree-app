import dagre from "dagre";

import type { FamilyGraph, FamilyGraphNode } from "../types";

const PERSON_NODE_WIDTH = 180;
const PERSON_NODE_HEIGHT = 76;
const FAMILY_NODE_SIZE = 28;

function dimensions(node: FamilyGraphNode) {
  if (node.type === "family-unit") {
    return { width: FAMILY_NODE_SIZE, height: FAMILY_NODE_SIZE };
  }

  return { width: PERSON_NODE_WIDTH, height: PERSON_NODE_HEIGHT };
}

export function applyDagreLayout(graph: FamilyGraph): FamilyGraph {
  const dagreGraph = new dagre.graphlib.Graph();
  dagreGraph.setDefaultEdgeLabel(() => ({}));
  dagreGraph.setGraph({ rankdir: "TB", nodesep: 44, ranksep: 76 });

  for (const node of graph.nodes) {
    dagreGraph.setNode(node.id, dimensions(node));
  }

  for (const edge of graph.edges) {
    dagreGraph.setEdge(edge.source, edge.target);
  }

  dagre.layout(dagreGraph);

  return {
    nodes: graph.nodes.map((node) => {
      const layoutNode = dagreGraph.node(node.id);
      const size = dimensions(node);

      return {
        ...node,
        position: {
          x: layoutNode.x - size.width / 2,
          y: layoutNode.y - size.height / 2,
        },
      };
    }),
    edges: graph.edges,
  };
}
