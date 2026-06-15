<template>
  <section v-if="person" class="relationship-form" aria-labelledby="relationships-title">
    <h3 id="relationships-title">Relationships</h3>

    <form class="relationship-create" @submit.prevent="submitRelationship">
      <label>
        Relationship
        <select v-model="relationshipMode">
          <option value="partner">Add partner</option>
          <option value="parent">Add parent</option>
          <option value="child">Add child</option>
        </select>
      </label>
      <label>
        Person
        <select v-model.number="relatedPersonId">
          <option :value="null" disabled>Select person</option>
          <option
            v-for="candidate in availablePeople"
            :key="candidate.id"
            :value="candidate.id"
          >
            {{ candidate.fullName }}
          </option>
        </select>
      </label>
      <button class="secondary-button" type="submit" :disabled="isSaving || !relatedPersonId">
        Add relationship
      </button>
    </form>

    <p v-if="error" class="form-error" role="alert">{{ error }}</p>

    <div v-if="personRelationships.length" class="relationship-list">
      <div
        v-for="relationship in personRelationships"
        :key="relationship.id"
        class="relationship-row"
      >
        <span>{{ relationshipLabel(relationship) }}</span>
        <button
          type="button"
          class="link-button"
          :disabled="isSaving"
          @click="removeRelationship(relationship.id)"
        >
          Remove
        </button>
      </div>
    </div>
  </section>
</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue";

import type { PersonDto, RelationshipDto } from "../tree/types";
import { createRelationship, deleteRelationship } from "./moderatorApi";

type RelationshipMode = "partner" | "parent" | "child";

export default defineComponent({
  name: "RelationshipForm",
  props: {
    person: {
      type: Object as PropType<PersonDto | null>,
      required: true,
    },
    people: {
      type: Array as PropType<PersonDto[]>,
      required: true,
    },
    relationships: {
      type: Array as PropType<RelationshipDto[]>,
      required: true,
    },
  },
  emits: {
    saved: () => true,
  },
  data() {
    return {
      error: "",
      isSaving: false,
      relatedPersonId: null as number | null,
      relationshipMode: "partner" as RelationshipMode,
    };
  },
  computed: {
    availablePeople(): PersonDto[] {
      if (!this.person) {
        return [];
      }

      return this.people.filter((candidate) => candidate.id !== this.person?.id);
    },
    peopleById(): Map<number, PersonDto> {
      return new Map(this.people.map((person) => [person.id, person]));
    },
    personRelationships(): RelationshipDto[] {
      if (!this.person) {
        return [];
      }

      return this.relationships.filter(
        (relationship) =>
          relationship.sourcePersonId === this.person?.id ||
          relationship.targetPersonId === this.person?.id,
      );
    },
  },
  methods: {
    async submitRelationship() {
      if (!this.person || this.relatedPersonId === null) {
        return;
      }

      this.error = "";
      this.isSaving = true;

      const sourcePersonId =
        this.relationshipMode === "parent" ? this.relatedPersonId : this.person.id;
      const targetPersonId =
        this.relationshipMode === "parent" ? this.person.id : this.relatedPersonId;

      try {
        await createRelationship({
          relationshipType:
            this.relationshipMode === "partner" ? "partner" : "parent_child",
          sourcePersonId,
          targetPersonId,
        });
        this.relatedPersonId = null;
        this.$emit("saved");
      } catch (error) {
        this.error = "Unable to save relationship";
      } finally {
        this.isSaving = false;
      }
    },
    async removeRelationship(relationshipId: number) {
      this.error = "";
      this.isSaving = true;

      try {
        await deleteRelationship(relationshipId);
        this.$emit("saved");
      } catch (error) {
        this.error = "Unable to remove relationship";
      } finally {
        this.isSaving = false;
      }
    },
    relationshipLabel(relationship: RelationshipDto): string {
      if (!this.person) {
        return "";
      }

      const source = this.peopleById.get(relationship.sourcePersonId);
      const target = this.peopleById.get(relationship.targetPersonId);

      if (relationship.type === "partner") {
        const partner =
          relationship.sourcePersonId === this.person.id ? target : source;
        return `Partner: ${partner?.fullName ?? "Unknown person"}`;
      }

      if (relationship.targetPersonId === this.person.id) {
        return `Parent: ${source?.fullName ?? "Unknown person"}`;
      }

      return `Child: ${target?.fullName ?? "Unknown person"}`;
    },
  },
});
</script>

<style scoped>
.relationship-form,
.relationship-create,
.relationship-list {
  display: grid;
  gap: 12px;
}

h3 {
  margin: 0;
  font-size: 1rem;
}

label {
  display: grid;
  gap: 6px;
  color: #52606d;
  font-size: 0.86rem;
  font-weight: 700;
}

select {
  min-height: 40px;
  padding: 8px 10px;
  border: 1px solid #bcccdc;
  border-radius: 6px;
  background: #ffffff;
  color: #1f2933;
  font: inherit;
}

.secondary-button {
  min-height: 40px;
  border: 1px solid #1f2933;
  border-radius: 6px;
  background: #ffffff;
  color: #1f2933;
  font-weight: 700;
  cursor: pointer;
}

.secondary-button:disabled,
.link-button:disabled {
  cursor: wait;
  opacity: 0.65;
}

.relationship-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 10px 0;
  border-top: 1px solid #edf2f7;
}

.link-button {
  border: 0;
  background: transparent;
  color: #b42318;
  font-weight: 700;
  cursor: pointer;
}

.form-error {
  margin: 0;
  color: #b42318;
  font-weight: 700;
}
</style>
