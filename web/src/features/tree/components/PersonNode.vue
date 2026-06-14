<template>
  <button class="person-node" type="button" @click="selectPerson">
    <span class="person-name">{{ data.person.fullName }}</span>
    <span v-if="lifeDates" class="life-dates">{{ lifeDates }}</span>
  </button>
</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue";

import type { PersonNodeData } from "../types";

export default defineComponent({
  name: "PersonNode",
  props: {
    data: {
      type: Object as PropType<PersonNodeData>,
      required: true,
    },
  },
  emits: {
    select: (_personId: number) => true,
  },
  computed: {
    lifeDates(): string {
      return [this.data.person.birthDate, this.data.person.deathDate]
        .filter(Boolean)
        .join(" - ");
    },
  },
  methods: {
    selectPerson() {
      this.$emit("select", this.data.person.id);
    },
  },
});
</script>

<style scoped>
.person-node {
  width: 180px;
  min-height: 76px;
  padding: 12px;
  border: 1px solid #bcccdc;
  border-radius: 8px;
  color: #1f2933;
  background: #ffffff;
  box-shadow: 0 10px 24px rgb(16 24 40 / 10%);
  cursor: pointer;
  text-align: left;
}

.person-node:hover,
.person-node:focus {
  border-color: #2f80ed;
  outline: 3px solid rgb(47 128 237 / 18%);
}

.person-name,
.life-dates {
  display: block;
}

.person-name {
  font-weight: 700;
}

.life-dates {
  margin-top: 4px;
  color: #52606d;
  font-size: 0.84rem;
}
</style>
