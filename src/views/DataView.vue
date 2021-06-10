<template>
  <div>
    <Visualization/>
  </div>
</template>

<script lang="ts">

import { Component, Vue } from 'vue-property-decorator'

import Visualization from '@/components/Visualization.vue'

@Component({
  components: {
    Visualization
  }
})
export default class DataView extends Vue {

}

</script>

<style scoped lang="scss">
</style>
