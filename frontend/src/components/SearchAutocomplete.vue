<template>
  <div class="search-autocomplete">
    <IconField class="p-input-icon-left w-full">
      <InputIcon class="pi pi-search" />
      <AutoComplete
        v-model="localQuery"
        :suggestions="displaySuggestions"
        :placeholder="placeholder"
        :loading="loading"
        :minLength="2"
        :delay="debounceMs"
        :completeOnFocus="false"
        :forceSelection="false"
        class="w-full"
        inputClass="w-full"
        @complete="handleComplete"
        @item-select="handleItemSelect"
      >
        <template #option="{ option }">
          <div class="suggestion-item-content">
            <i class="pi pi-search suggestion-icon" />
            <span class="suggestion-text">{{ option }}</span>
          </div>
        </template>
        <template #empty>
          <div class="empty-message">
            <i class="pi pi-info-circle" />
            <span>Không tìm thấy gợi ý</span>
          </div>
        </template>
      </AutoComplete>
    </IconField>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import AutoComplete from "primevue/autocomplete";
import IconField from "primevue/iconfield";
import InputIcon from "primevue/inputicon";
import { casesService } from "@/services/cases";

interface Props {
  modelValue: string;
  placeholder?: string;
  debounceMs?: number;
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: "Tìm kiếm...",
  debounceMs: 300,
});

const emit = defineEmits<{
  "update:modelValue": [value: string];
}>();

const localQuery = ref(props.modelValue);
const suggestions = ref<string[]>([]);
const displaySuggestions = ref<string[]>([]);
const loading = ref(false);

// Watch for external changes to modelValue
watch(
  () => props.modelValue,
  (newVal) => {
    if (newVal !== localQuery.value) {
      localQuery.value = newVal;
    }
  },
);

// Watch for local changes and emit to parent
watch(localQuery, (newVal) => {
  emit("update:modelValue", newVal as string);
});

function getLastToken(query: string): string {
  const tokens = query.trim().split(/\s+/);
  return tokens[tokens.length - 1] || "";
}

function buildSuggestionText(suggestion: string): string {
  const tokens = (localQuery.value as string).trim().split(/\s+/);
  if (tokens.length === 0) return suggestion;
  tokens[tokens.length - 1] = suggestion;
  return tokens.join(" ");
}

async function handleComplete(event: any) {
  const query = event.query || localQuery.value;
  const lastToken = getLastToken(query);

  if (!lastToken || lastToken.length < 2) {
    suggestions.value = [];
    displaySuggestions.value = [];
    return;
  }

  loading.value = true;
  try {
    const results = await casesService.getSearchSuggestions(lastToken);
    suggestions.value = results || [];
    displaySuggestions.value = suggestions.value.map((s) =>
      buildSuggestionText(s),
    );
  } catch {
    suggestions.value = [];
    displaySuggestions.value = [];
  } finally {
    loading.value = false;
  }
}

function handleItemSelect(event: any) {
  localQuery.value = event.value;
  emit("update:modelValue", event.value);
}
</script>

<style scoped>
.search-autocomplete {
  position: relative;
  width: 100%;
}

/* Ensure AutoComplete fills its container — globals.css .p-inputtext rules
   already set the background/border/color; we only add layout overrides here. */
:deep(.p-autocomplete) {
  width: 100%;
}

:deep(.p-autocomplete-input) {
  width: 100%;
}

/* Suggestion item */
.suggestion-item-content {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 4px 0;
}

.suggestion-icon {
  color: var(--muted-foreground);
  font-size: 14px;
  flex-shrink: 0;
}

.suggestion-text {
  color: var(--foreground);
  font-size: 14px;
  flex: 1;
}

/* Empty message */
.empty-message {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  color: var(--muted-foreground);
  font-size: 14px;
}

/* Dropdown panel — reconciles with globals.css .p-autocomplete-panel overrides */
:deep(.p-autocomplete-panel) {
  border-radius: var(--radius);
  box-shadow:
    0 4px 6px -1px var(--shadow-grey),
    0 2px 4px -1px var(--shadow-grey);
  margin-top: 4px;
  animation: dropdown-in 0.2s ease-out;
}

:deep(.p-autocomplete-items) {
  padding: 8px 0;
}

:deep(.p-autocomplete-item) {
  padding: 10px 16px;
  transition: background-color 0.15s ease;
}

:deep(.p-autocomplete-item:hover),
:deep(.p-autocomplete-item.p-focus) {
  background-color: var(--secondary) !important;
}

@keyframes dropdown-in {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
