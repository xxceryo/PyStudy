<script setup lang="ts">
import { useRouter } from 'vue-router'
import { auth } from '../auth'

const router = useRouter()

async function logout(): Promise<void> {
  auth.clearSession()
  await router.push({ name: 'login' })
}
</script>

<template>
  <main class="market-page">
    <header class="market-header">
      <div class="brand-lockup"><span class="brand-mark">LS</span> LOOT//SHIFT</div>
      <nav><span>市场</span><span>库存</span><span>交易</span></nav>
      <div class="player-menu">
        <span class="status-dot"></span>
        <div><small>PLAYER ONLINE</small><strong>{{ auth.state.user?.nickname || auth.state.user?.username }}</strong></div>
        <button type="button" @click="logout">退出</button>
      </div>
    </header>

    <section class="market-shell">
      <div class="market-meta"><span>MARKET BUILD // 0.1</span><span>NODE STATUS: ONLINE</span></div>
      <div class="empty-state">
        <div class="pixel-cube"><span></span><span></span><span></span></div>
        <p class="eyebrow">NEW ZONE UNLOCKING</p>
        <h1>市场正在构建中</h1>
        <p>身份验证节点已经上线。虚拟物品陈列、交易与库存功能将在下一个版本开放。</p>
        <div class="progress-track"><i></i></div>
        <small>CORE SYSTEMS 32%</small>
      </div>
      <div class="future-grid">
        <article><span>01</span><h3>发现稀有掉落</h3><p>浏览由玩家发布的虚拟物品。</p></article>
        <article><span>02</span><h3>安全发起交易</h3><p>透明记录每一次物品交换。</p></article>
        <article><span>03</span><h3>管理个人库存</h3><p>集中展示你的数字收藏。</p></article>
      </div>
    </section>
  </main>
</template>
