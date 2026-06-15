<template>
  <aside class="edit-drawer" aria-label="Edit person">
    <header>
      <h2>{{ person ? "Edit person" : "Add person" }}</h2>
      <button type="button" class="close-button" aria-label="Close editor" @click="$emit('close')">
        x
      </button>
    </header>

    <form class="person-form" @submit.prevent="submitPerson">
      <label>
        Full name
        <input v-model="form.fullName" required />
      </label>
      <label>
        Birth date
        <input v-model="form.birthDate" type="date" />
      </label>
      <label>
        Death date
        <input v-model="form.deathDate" type="date" />
      </label>
      <label>
        Notes
        <textarea v-model="form.notes" rows="4" />
      </label>

      <p v-if="error" class="form-error" role="alert">{{ error }}</p>

      <button class="primary-button" type="submit" :disabled="isSaving">
        {{ person ? "Save person" : "Create person" }}
      </button>
    </form>

    <RelationshipForm
      v-if="person"
      :people="people"
      :person="person"
      :relationships="relationships"
      @saved="$emit('saved')"
    />
  </aside>
</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue";

import type { PersonDto, RelationshipDto } from "../tree/types";
import { createPerson, updatePerson, type PersonInput } from "./moderatorApi";
import RelationshipForm from "./RelationshipForm.vue";

interface PersonFormState {
  fullName: string;
  birthDate: string;
  deathDate: string;
  notes: string;
}

function formFromPerson(person: PersonDto | null): PersonFormState {
  return {
    fullName: person?.fullName ?? "",
    birthDate: person?.birthDate ?? "",
    deathDate: person?.deathDate ?? "",
    notes: person?.notes ?? "",
  };
}

function toPersonInput(form: PersonFormState): PersonInput {
  return {
    fullName: form.fullName.trim(),
    birthDate: form.birthDate || null,
    deathDate: form.deathDate || null,
    notes: form.notes.trim() || null,
  };
}

export default defineComponent({
  name: "EditPersonDrawer",
  components: {
    RelationshipForm,
  },
  props: {
    person: {
      type: Object as PropType<PersonDto | null>,
      default: null,
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
    close: () => true,
    saved: () => true,
  },
  data() {
    return {
      error: "",
      form: formFromPerson(this.person),
      isSaving: false,
    };
  },
  watch: {
    person(nextPerson: PersonDto | null) {
      this.form = formFromPerson(nextPerson);
      this.error = "";
    },
  },
  methods: {
    async submitPerson() {
      const payload = toPersonInput(this.form);

      if (!payload.fullName) {
        this.error = "Full name is required";
        return;
      }

      this.error = "";
      this.isSaving = true;

      try {
        if (this.person) {
          await updatePerson(this.person.id, payload);
        } else {
          await createPerson(payload);
          this.form = formFromPerson(null);
        }

        this.$emit("saved");
      } catch (error) {
        this.error = "Unable to save person";
      } finally {
        this.isSaving = false;
      }
    },
  },
});
</script>

<style scoped>
.edit-drawer {
  display: grid;
  align-content: start;
  gap: 20px;
  min-width: 320px;
  max-width: 360px;
  padding: 24px;
  border-left: 1px solid #d9e2ec;
  background: #ffffff;
}

header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

h2 {
  margin: 0;
  font-size: 1.25rem;
}

.close-button {
  width: 34px;
  height: 34px;
  border: 1px solid #bcccdc;
  border-radius: 6px;
  background: #ffffff;
  cursor: pointer;
}

.person-form {
  display: grid;
  gap: 14px;
}

label {
  display: grid;
  gap: 6px;
  color: #52606d;
  font-size: 0.86rem;
  font-weight: 700;
}

input,
textarea {
  width: 100%;
  padding: 9px 12px;
  border: 1px solid #bcccdc;
  border-radius: 6px;
  background: #ffffff;
  color: #1f2933;
  font: inherit;
}

textarea {
  resize: vertical;
}

input:focus,
textarea:focus {
  border-color: #2f80ed;
  outline: 3px solid rgb(47 128 237 / 18%);
}

.primary-button {
  min-height: 42px;
  border: 0;
  border-radius: 6px;
  background: #1f2933;
  color: #ffffff;
  font-weight: 700;
  cursor: pointer;
}

.primary-button:disabled {
  cursor: wait;
  opacity: 0.7;
}

.form-error {
  margin: 0;
  color: #b42318;
  font-weight: 700;
}

@media (max-width: 760px) {
  .edit-drawer {
    min-width: 0;
    max-width: none;
    border-left: 0;
    border-top: 1px solid #d9e2ec;
  }
}
</style>
