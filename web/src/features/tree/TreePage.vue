<template>
  <main class="tree-page">
    <section class="tree-stage">
      <header class="tree-header">
        <h1>Family Tree</h1>
        <div class="tree-actions">
          <PersonSearch
            v-if="tree.people.length"
            :people="tree.people"
            @select-person="selectPerson"
          />
          <button
            v-if="canModerate"
            class="add-person-button"
            type="button"
            @click="openCreateDrawer"
          >
            Add person
          </button>
        </div>
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
          v-if="selectedPerson && !isEditorOpen"
          :people="tree.people"
          :person="selectedPerson"
          :relationships="tree.relationships"
          :can-edit="canModerate"
          @close="selectedPersonId = null"
          @edit="openEditDrawer"
        />
        <EditPersonDrawer
          v-if="isEditorOpen"
          :people="tree.people"
          :person="editingPerson"
          :relationships="tree.relationships"
          @close="closeEditor"
          @saved="handleEditorSaved"
        />
      </div>
    </section>
  </main>
</template>

<script lang="ts">
import { defineComponent } from "vue";

import EditPersonDrawer from "../editor/EditPersonDrawer.vue";
import PersonDetailsPanel from "../person/PersonDetailsPanel.vue";
import PersonSearch from "../search/PersonSearch.vue";
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
    EditPersonDrawer,
    FamilyTreeCanvas,
    PersonDetailsPanel,
    PersonSearch,
  },
  data() {
    return {
      editorPersonId: null as number | null,
      error: "",
      isEditorOpen: false,
      isLoading: true,
      selectedPersonId: null as number | null,
      tree: emptyTree,
    };
  },
  computed: {
    canModerate(): boolean {
      return this.tree.viewerRole === "moderator" || this.tree.viewerRole === "owner";
    },
    editingPerson(): PersonDto | null {
      if (this.editorPersonId === null) {
        return null;
      }

      return (
        this.tree.people.find((person) => person.id === this.editorPersonId) ?? null
      );
    },
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
    await this.loadTree();
  },
  methods: {
    closeEditor() {
      this.isEditorOpen = false;
      this.editorPersonId = null;
    },
    async handleEditorSaved() {
      await this.loadTree();
    },
    async loadTree() {
      this.isLoading = true;
      this.error = "";

      try {
        this.tree = await fetchTree();
      } catch (error) {
        this.error = "Unable to load family tree";
      } finally {
        this.isLoading = false;
      }
    },
    openCreateDrawer() {
      this.editorPersonId = null;
      this.isEditorOpen = true;
    },
    openEditDrawer(personId: number) {
      this.editorPersonId = personId;
      this.isEditorOpen = true;
    },
    selectPerson(personId: number) {
      this.selectedPersonId = personId;
      this.closeEditor();
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
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: center;
  gap: 16px;
}

h1 {
  margin: 0;
  font-size: 1.8rem;
  line-height: 1.15;
}

.tree-actions {
  display: flex;
  align-items: start;
  justify-content: end;
  gap: 12px;
}

.add-person-button {
  min-height: 40px;
  padding: 0 14px;
  border: 0;
  border-radius: 6px;
  background: #1f2933;
  color: #ffffff;
  font-weight: 700;
  cursor: pointer;
  white-space: nowrap;
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

  .tree-header {
    grid-template-columns: 1fr;
  }

  .tree-actions {
    display: grid;
    justify-content: stretch;
  }

  .tree-workspace {
    grid-template-columns: 1fr;
  }
}
</style>
