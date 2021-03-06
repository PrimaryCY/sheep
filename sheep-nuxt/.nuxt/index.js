import Vue from 'vue'
import Vuex from 'vuex'
import Meta from 'vue-meta'
import ClientOnly from 'vue-client-only'
import NoSsr from 'vue-no-ssr'
import { createRouter } from './router.js'
import NuxtChild from './components/nuxt-child.js'
import NuxtError from '../layouts/error.vue'
import Nuxt from './components/nuxt.js'
import App from './App.js'
import { setContext, getLocation, getRouteData, normalizeError } from './utils'
import { createStore } from './store.js'

/* Plugins */

import nuxt_plugin_cookieuniversalnuxt_69d7639a from 'nuxt_plugin_cookieuniversalnuxt_69d7639a' // Source: ./cookie-universal-nuxt.js (mode: 'all')
import nuxt_plugin_router_4f5cbc06 from 'nuxt_plugin_router_4f5cbc06' // Source: ./router.js (mode: 'all')
import nuxt_plugin_nuxtcookies_2be8578a from 'nuxt_plugin_nuxtcookies_2be8578a' // Source: ../plugins/nuxt-cookies (mode: 'all')
import nuxt_plugin_vueparticles_b91bd920 from 'nuxt_plugin_vueparticles_b91bd920' // Source: ../plugins/vue-particles (mode: 'client')
import nuxt_plugin_nprogress_2ce44436 from 'nuxt_plugin_nprogress_2ce44436' // Source: ../plugins/nprogress (mode: 'client')
import nuxt_plugin_element_0d2eee9a from 'nuxt_plugin_element_0d2eee9a' // Source: ../plugins/element/element (mode: 'all')
import nuxt_plugin_vueinfinitescroll_18d3fb29 from 'nuxt_plugin_vueinfinitescroll_18d3fb29' // Source: ../plugins/vue-infinite-scroll (mode: 'client')
import nuxt_plugin_axios_3566aa80 from 'nuxt_plugin_axios_3566aa80' // Source: ../plugins/axios (mode: 'all')
import nuxt_plugin_util_925ee814 from 'nuxt_plugin_util_925ee814' // Source: ../plugins/util (mode: 'all')
import nuxt_plugin_ant_5e4622b1 from 'nuxt_plugin_ant_5e4622b1' // Source: ../plugins/ant (mode: 'all')

// Component: <ClientOnly>
Vue.component(ClientOnly.name, ClientOnly)

// TODO: Remove in Nuxt 3: <NoSsr>
Vue.component(NoSsr.name, {
  ...NoSsr,
  render (h, ctx) {
    if (process.client && !NoSsr._warned) {
      NoSsr._warned = true

      console.warn('<no-ssr> has been deprecated and will be removed in Nuxt 3, please use <client-only> instead')
    }
    return NoSsr.render(h, ctx)
  }
})

// Component: <NuxtChild>
Vue.component(NuxtChild.name, NuxtChild)
Vue.component('NChild', NuxtChild)

// Component NuxtLink is imported in server.js or client.js

// Component: <Nuxt>
Vue.component(Nuxt.name, Nuxt)

Vue.use(Meta, {"keyName":"head","attribute":"data-n-head","ssrAttribute":"data-n-head-ssr","tagIDKeyName":"hid"})

const defaultTransition = {"name":"page","mode":"out-in","appear":false,"appearClass":"appear","appearActiveClass":"appear-active","appearToClass":"appear-to"}

const originalRegisterModule = Vuex.Store.prototype.registerModule
const baseStoreOptions = { preserveState: process.client }

function registerModule (path, rawModule, options = {}) {
  return originalRegisterModule.call(this, path, rawModule, { ...baseStoreOptions, ...options })
}

async function createApp(ssrContext, config = {}) {
  const router = await createRouter(ssrContext)

  const store = createStore(ssrContext)
  // Add this.$router into store actions/mutations
  store.$router = router

  // Fix SSR caveat https://github.com/nuxt/nuxt.js/issues/3757#issuecomment-414689141
  store.registerModule = registerModule

  // Create Root instance

  // here we inject the router and store to all child components,
  // making them available everywhere as `this.$router` and `this.$store`.
  const app = {
    head: {"title":"羊绒衫","meta":[{"charset":"utf-8"},{"name":"viewport","content":"width=device-width, initial-scale=1"},{"name":"keywords","content":"博客,blog,羊绒衫官网,小羊,分享,好玩,图文编辑软件,图文创作,创作软件,原创社区,小说,散文,写作,阅读"},{"hid":"description","name":"description","content":"My rad Nuxt.js project"}],"link":[{"rel":"icon","type":"image\u002Fx-icon","href":"\u002Ffavicon.png"}],"script":[{"src":"http:\u002F\u002Flibs.baidu.com\u002Fjquery\u002F1.8.3\u002Fjquery.min.js"},{"src":"http:\u002F\u002Fat.alicdn.com\u002Ft\u002Ffont_1739386_3bmedkb9dpo.js"}],"bodyAttrs":{"class":"left-sidebar is-desktop is-1200px"},"style":[]},

    store,
    router,
    nuxt: {
      defaultTransition,
      transitions: [defaultTransition],
      setTransitions (transitions) {
        if (!Array.isArray(transitions)) {
          transitions = [transitions]
        }
        transitions = transitions.map((transition) => {
          if (!transition) {
            transition = defaultTransition
          } else if (typeof transition === 'string') {
            transition = Object.assign({}, defaultTransition, { name: transition })
          } else {
            transition = Object.assign({}, defaultTransition, transition)
          }
          return transition
        })
        this.$options.nuxt.transitions = transitions
        return transitions
      },

      err: null,
      dateErr: null,
      error (err) {
        err = err || null
        app.context._errored = Boolean(err)
        err = err ? normalizeError(err) : null
        let nuxt = app.nuxt // to work with @vue/composition-api, see https://github.com/nuxt/nuxt.js/issues/6517#issuecomment-573280207
        if (this) {
          nuxt = this.nuxt || this.$options.nuxt
        }
        nuxt.dateErr = Date.now()
        nuxt.err = err
        // Used in src/server.js
        if (ssrContext) {
          ssrContext.nuxt.error = err
        }
        return err
      }
    },
    ...App
  }

  // Make app available into store via this.app
  store.app = app

  const next = ssrContext ? ssrContext.next : location => app.router.push(location)
  // Resolve route
  let route
  if (ssrContext) {
    route = router.resolve(ssrContext.url).route
  } else {
    const path = getLocation(router.options.base, router.options.mode)
    route = router.resolve(path).route
  }

  // Set context to app.context
  await setContext(app, {
    store,
    route,
    next,
    error: app.nuxt.error.bind(app),
    payload: ssrContext ? ssrContext.payload : undefined,
    req: ssrContext ? ssrContext.req : undefined,
    res: ssrContext ? ssrContext.res : undefined,
    beforeRenderFns: ssrContext ? ssrContext.beforeRenderFns : undefined,
    ssrContext
  })

  function inject(key, value) {
    if (!key) {
      throw new Error('inject(key, value) has no key provided')
    }
    if (value === undefined) {
      throw new Error(`inject('${key}', value) has no value provided`)
    }

    key = '$' + key
    // Add into app
    app[key] = value
    // Add into context
    if (!app.context[key]) {
      app.context[key] = value
    }

    // Add into store
    store[key] = app[key]

    // Check if plugin not already installed
    const installKey = '__nuxt_' + key + '_installed__'
    if (Vue[installKey]) {
      return
    }
    Vue[installKey] = true
    // Call Vue.use() to install the plugin into vm
    Vue.use(() => {
      if (!Object.prototype.hasOwnProperty.call(Vue.prototype, key)) {
        Object.defineProperty(Vue.prototype, key, {
          get () {
            return this.$root.$options[key]
          }
        })
      }
    })
  }

  // Inject runtime config as $config
  inject('config', config)

  if (process.client) {
    // Replace store state before plugins execution
    if (window.__NUXT__ && window.__NUXT__.state) {
      store.replaceState(window.__NUXT__.state)
    }
  }

  // Add enablePreview(previewData = {}) in context for plugins
  if (process.static && process.client) {
    app.context.enablePreview = function (previewData = {}) {
      app.previewData = Object.assign({}, previewData)
      inject('preview', previewData)
    }
  }
  // Plugin execution

  if (typeof nuxt_plugin_cookieuniversalnuxt_69d7639a === 'function') {
    await nuxt_plugin_cookieuniversalnuxt_69d7639a(app.context, inject)
  }

  if (typeof nuxt_plugin_router_4f5cbc06 === 'function') {
    await nuxt_plugin_router_4f5cbc06(app.context, inject)
  }

  if (typeof nuxt_plugin_nuxtcookies_2be8578a === 'function') {
    await nuxt_plugin_nuxtcookies_2be8578a(app.context, inject)
  }

  if (process.client && typeof nuxt_plugin_vueparticles_b91bd920 === 'function') {
    await nuxt_plugin_vueparticles_b91bd920(app.context, inject)
  }

  if (process.client && typeof nuxt_plugin_nprogress_2ce44436 === 'function') {
    await nuxt_plugin_nprogress_2ce44436(app.context, inject)
  }

  if (typeof nuxt_plugin_element_0d2eee9a === 'function') {
    await nuxt_plugin_element_0d2eee9a(app.context, inject)
  }

  if (process.client && typeof nuxt_plugin_vueinfinitescroll_18d3fb29 === 'function') {
    await nuxt_plugin_vueinfinitescroll_18d3fb29(app.context, inject)
  }

  if (typeof nuxt_plugin_axios_3566aa80 === 'function') {
    await nuxt_plugin_axios_3566aa80(app.context, inject)
  }

  if (typeof nuxt_plugin_util_925ee814 === 'function') {
    await nuxt_plugin_util_925ee814(app.context, inject)
  }

  if (typeof nuxt_plugin_ant_5e4622b1 === 'function') {
    await nuxt_plugin_ant_5e4622b1(app.context, inject)
  }

  // Lock enablePreview in context
  if (process.static && process.client) {
    app.context.enablePreview = function () {
      console.warn('You cannot call enablePreview() outside a plugin.')
    }
  }

  // If server-side, wait for async component to be resolved first
  if (process.server && ssrContext && ssrContext.url) {
    await new Promise((resolve, reject) => {
      router.push(ssrContext.url, resolve, (err) => {
        // https://github.com/vuejs/vue-router/blob/v3.4.3/src/util/errors.js
        if (!err._isRouter) return reject(err)
        if (err.type !== 2 /* NavigationFailureType.redirected */) return resolve()

        // navigated to a different route in router guard
        const unregister = router.afterEach(async (to, from) => {
          ssrContext.url = to.fullPath
          app.context.route = await getRouteData(to)
          app.context.params = to.params || {}
          app.context.query = to.query || {}
          unregister()
          resolve()
        })
      })
    })
  }

  return {
    store,
    app,
    router
  }
}

export { createApp, NuxtError }
