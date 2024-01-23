<script setup lang="ts">
import * as childProcess from 'child_process';

const { data: renderDateTime } = useAsyncData('renderDateTime', async () => {
  const dateTime = new Date().toUTCString()
  return dateTime
})

const { data: commitHash } = useAsyncData('commitHash', async () => {
    var commitHash = '';
    try {
        commitHash = childProcess
        .execSync('git rev-parse --short HEAD')
        .toString().trim();
    } catch (e) {
        console.error(e);
    }   
  return commitHash
})

</script>

<template>
Version Information: Commit <code>{{ commitHash }}</code> rendered on {{ renderDateTime }}
</template>
