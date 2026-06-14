<template>
  <main class="tree-page">
    <section class="tree-stage">
      <header class="tree-header">
        <h1>Family Tree</h1>
      </header>

      <p v-if="error" class="error" role="alert">{{ error }}</p>
      <div v-else-if="isLoading" class="loading" role="status">Loading tree</div>
      <div v-else class="tree-workspace">
        <FamilyTreeCanvas
          class="tree-view"
          :graph="graph"
          @select-person="selectPerson"
        />
        <PersonDetailsPanel
          v-if="selectedPerson"
          :people="tree.people"
          :person="selectedPerson"
          :relationships="tree.relationships"
          @close="selectedPersonId = null"
        />
      </div>
    </section>
  </main>
</template>

<script lang="ts">
import { defineComponent } from "vue";

import PersonDetailsPanel from "../person/PersonDetailsPanel.vue";
import { fetchTree } from "./api";
import FamilyTreeCanvas from "./components/FamilyTreeCanvas.vue";
import { applyDagreLayout } from "./layout/applyDagreLayout";
import { buildFamilyGraph } from "./layout/buildFamilyGraph";
import type { FamilyGraph, PersonDto, TreeDto } from "./types";

const emptyTree: TreeDto = {
  viewerRole: "viewer",
  people: [],
  relationships: [],
};

export default defineComponent({
  name: "TreePage",
  components: {
    FamilyTreeCanvas,
    PersonDetailsPanel,
  },
  data() {
    return {
      error: "",
      isLoading: true,
      selectedPersonId: null as number | null,
      tree: emptyTree,
    };
  },
  computed: {
    graph(): FamilyGraph {
      return applyDagreLayout(
        buildFamilyGraph(this.tree.people, this.tree.relationships),
      );
    },
    selectedPerson(): PersonDto | null {
      if (this.selectedPersonId === null) {
        return null;
      }

      return (
        this.tree.people.find((person) => person.id === this.selectedPersonId) ??
        null
      );
    },
  },
  async mounted() {
    try {
      this.tree = await fetchTree();
    } catch (error) {
      this.error = "Unable to load family tree";
    } finally {
      this.isLoading = false;
    }
  },
  methods: {
    selectPerson(personId: number) {
      this.selectedPersonId = personId;
    },
  },
});
</script>

<style scoped>
.tree-page {
  min-height: 100vh;
  background: #f5f7fa;
}

.tree-stage {
  display: grid;
  gap: 18px;
  width: min(100%, 1280px);
  margin: 0 auto;
  padding: 24px;
}

.tree-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

h1 {
  margin: 0;
  font-size: 1.8rem;
  line-height: 1.15;
}

.tree-workspace {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  min-height: 620px;
  overflow: hidden;
  border: 1px solid #d9e2ec;
  border-radius: 8px;
  background: #ffffff;
  box-shadow: 0 16px 40px rgb(16 24 40 / 8%);
}

.tree-view {
  min-width: 0;
  border: 0;
  border-radius: 0;
}

.loading,
.error {
  width: min(100%, 420px);
  padding: 16px;
  border: 1px solid #d9e2ec;
  border-radius: 8px;
  background: #ffffff;
}

@media (max-width: 760px) {
  .tree-stage {
    padding: 16px;
  }

  .tree-workspace {
    grid-template-columns: 1fr;
  }
}
</style>
