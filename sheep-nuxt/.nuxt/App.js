import Vue from 'vue'
import NuxtLoading from './components/nuxt-loading.vue'

import '..\\static\\css\\reset.css'

import '..\\static\\css\\5grid\\core.css'

import '..\\static\\css\\style.css'

import '..\\static\\css\\5grid\\core-desktop.css'

import '..\\static\\css\\style-desktop.css'

import '..\\static\\css\\5grid\\core-1200px.css'

import '..\\static\\css\\style-1200px.css'


import _6f6c098b from '..\\layouts\\default.vue'

const layouts = { "_default": _6f6c098b }



export default {
  head: {"title":"sheep-nuxt","meta":[{"charset":"utf-8"},{"name":"viewport","content":"width=device-width, initial-scale=1"},{"hid":"description","name":"description","content":"My rad Nuxt.js project"}],"link":[{"rel":"icon","type":"image\u002Fx-icon","href":"\u002Ffavicon.png"}],"script":[{"src":"http:\u002F\u002Flibs.baidu.com\u002Fjquery\u002F1.8.3\u002Fjquery.min.js"},{"src":"http:\u002F\u002Fat.alicdn.com\u002Ft\u002Ffont_1739386_3bmedkb9dpo.js"}],"bodyAttrs":{"class":"left-sidebar is-desktop is-1200px"},"style":[]},
  render(h, props) {
    const loadingEl = h('nuxt-loading', { ref: 'loading' })
    const layoutEl = h(this.layout || 'nuxt')
    const templateEl = h('div', {
      domProps: {
        id: '__layout'
      },
      key: this.layoutName
    }, [ layoutEl ])

    const transitionEl = h('transition', {
      props: {
        name: 'layout',
        mode: 'out-in'
      }
    }, [ templateEl ])

    return h('div',{
      domProps: {
        id: '__nuxt'
      }
    }, [
      loadingEl,
      transitionEl
    ])
  },
  data: () => ({
    layout: null,
    layoutName: ''
  }),
  beforeCreate () {
    Vue.util.defineReactive(this, 'nuxt', this.$options.nuxt)
  },
  created () {
    // Add this.$nuxt in child instances
    Vue.prototype.$nuxt = this
    // add to window so we can listen when ready
    if (typeof window !== 'undefined') {
      window.$nuxt = this
    }
    // Add $nuxt.error()
    this.error = this.nuxt.error
  },
  
  mounted () {
    this.$loading = this.$refs.loading
  },
  watch: {
    'nuxt.err': 'errorChanged'
  },
  
  methods: {
    
    errorChanged () {
      if (this.nuxt.err && this.$loading) {
        if (this.$loading.fail) this.$loading.fail()
        if (this.$loading.finish) this.$loading.finish()
      }
    },
    
    
    setLayout(layout) {
      if (!layout || !layouts['_' + layout]) {
        layout = 'default'
      }
      this.layoutName = layout
      this.layout = layouts['_' + layout]
      return this.layout
    },
    loadLayout(layout) {
      if (!layout || !layouts['_' + layout]) {
        layout = 'default'
      }
      return Promise.resolve(layouts['_' + layout])
    }
    
  },
  components: {
    NuxtLoading
  }
}
