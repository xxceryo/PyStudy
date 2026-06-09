<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ApiError } from '../api'
import { auth } from '../auth'

const route = useRoute()
const router = useRouter()
const username = ref('')
const password = ref('')
const errorMessage = ref('')
const submitting = ref(false)
const registrationComplete = computed(() => route.query.registered === '1')

async function submit(): Promise<void> {
  errorMessage.value = ''
  submitting.value = true
  try {
    await auth.login(username.value, password.value)
    const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : '/'
    await router.push(redirect)
  } catch (error) {
    errorMessage.value = error instanceof ApiError ? error.message : '无法连接到市场服务器'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <main class="auth-page">
    <section class="auth-story">
      <div class="brand-lockup"><span class="brand-mark">LS</span> LOOT//SHIFT</div>
      <div class="story-copy">
        <p class="eyebrow">PLAYER-TO-PLAYER MARKET // ONLINE</p>
        <h1>你的装备。<br><span>你的价格。</span></h1>
        <p class="story-text">一个为虚拟物品打造的可信交易市场。发现稀有掉落，完成下一次交换。</p>
      </div>
      <div class="market-ticker">
        <span>安全交易</span><strong>24/7</strong><span>市场状态</span><strong class="online">ONLINE</strong>
      </div>
    </section>

    <section class="auth-panel">
      <div class="panel-inner">
        <p class="panel-code">ACCESS PORTAL // 01</p>
        <h2>欢迎回来，玩家</h2>
        <p class="panel-intro">登录并继续你的交易进度。</p>
        <p v-if="registrationComplete" class="notice success">账号创建成功，现在可以进入市场。</p>
        <p v-if="errorMessage" class="notice error">{{ errorMessage }}</p>
        <form @submit.prevent="submit">
          <label>
            <span>用户名</span>
            <input v-model.trim="username" autocomplete="username" minlength="3" maxlength="50" required placeholder="输入玩家代号">
          </label>
          <label>
            <span>密码</span>
            <input v-model="password" type="password" autocomplete="current-password" minlength="8" maxlength="72" required placeholder="输入访问密码">
          </label>
          <button class="primary-button" :disabled="submitting" type="submit">
            {{ submitting ? '连接中...' : '进入市场' }} <span>→</span>
          </button>
        </form>
        <p class="switch-copy">还没有玩家档案？ <RouterLink to="/register">创建账号</RouterLink></p>
      </div>
    </section>
  </main>
</template>
