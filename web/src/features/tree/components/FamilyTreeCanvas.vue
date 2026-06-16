<template>
  <div class="tree-canvas">
    <VueFlow
      class="tree-flow"
      :edges="graph.edges"
      fit-view-on-init
      :nodes="graph.nodes"
      :node-types="nodeTypes"
      @node-click="onNodeClick"
    >
      <template #node-person="{ data }">
        <PersonNode :data="data" @select="selectPerson" />
      </template>
      <template #node-family-unit>
        <div aria-hidden="true" class="family-unit-node"></div>
      </template>
      <Background />
      <Controls />
    </VueFlow>
  </div>
</template>

<script lang="ts">
import "@vue-flow/core/dist/style.css";
import "@vue-flow/core/dist/theme-default.css";

import { Background } from "@vue-flow/background";
import { Controls } from "@vue-flow/controls";
import { VueFlow, type NodeMouseEvent } from "@vue-flow/core";
import { defineComponent, type PropType } from "vue";

import type { FamilyGraph, PersonNodeData } from "../types";
import PersonNode from "./PersonNode.vue";

export default defineComponent({
  name: "FamilyTreeCanvas",
  components: {
    Background,
    Controls,
    PersonNode,
    VueFlow,
  },
  props: {
    graph: {
      type: Object as PropType<FamilyGraph>,
      required: true,
    },
  },
  emits: {
    "select-person": (_personId: number) => true,
  },
  data() {
    return {
      nodeTypes: {},
    };
  },
  methods: {
    selectPerson(personId: number) {
      this.$emit("select-person", personId);
    },
    onNodeClick(event: NodeMouseEvent) {
      if (event.node.type !== "person") {
        return;
      }

      const data = event.node.data as PersonNodeData;
      this.selectPerson(data.person.id);
    },
  },
});
</script>

<style scoped>
.tree-canvas {
  position: relative;
  min-height: 620px;
  overflow: hidden;
  border: 1px solid #d9e2ec;
  border-radius: 8px;
  background: #f8fafc;
}

.tree-flow {
  min-height: 620px;
}

.family-unit-node {
  width: 24px;
  height: 24px;
  border: 3px solid #52606d;
  border-radius: 999px;
  background: #ffffff;
}
</style>
