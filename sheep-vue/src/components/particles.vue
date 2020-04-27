
<template>
	<div id='particles-js'></div>
</template>

<script>
	export default {
		name: 'ParticlesJS',
		mounted () {
			require('particles.js')
			this.$nextTick(() => {
				this.initParticlesJS()
			})
		},

		methods: {
			initParticlesJS () {
				/* eslint-disable */
				particlesJS('particles-js', {

					"particles": {
						"number": {
							"value": 80,
							"density": {
								"enable": true,
								"value_area": 800
							}
						},
						"color": {
							"value": "#000000"
						},
						"shape": {
							"type": "circle",
							"stroke": {
								"width": 0,
								"color": "#000000"
							},
							"polygon": {
								"nb_sides": 5
							},
							"image": {
								"src": "img/github.svg",
								"width": 100,
								"height": 100
							}
						},
						"opacity": {
							"value": 0.24837156385953366,
							"random": false,
							"anim": {
								"enable": false,
								"speed": 1,
								"opacity_min": 0.1,
								"sync": false
							}
						},
						"size": {
							"value": 3,
							"random": true,
							"anim": {
								"enable": false,
								"speed": 40,
								"size_min": 0.1,
								"sync": false
							}
						},
						"line_linked": {
							"enable": true,
							"distance": 100,
							"color": "#373737",
							"opacity": 0.745114691578601,
							"width": 0.6409588744762158
						},
						"move": {
							"enable": true,
							"speed": 6.409588744762158,
							"direction": "none",
							"random": false,
							"straight": false,
							"out_mode": "out",
							"bounce": false,
							"attract": {
								"enable": false,
								"rotateX": 600,
								"rotateY": 1200
							}
						}
					},
					"interactivity": {
						"detect_on": "canvas",
						"events": {
							"onhover": {
								"enable": true,
								"mode": "repulse"
							},
							"onclick": {
								"enable": true,
								"mode": "push"
							},
							"resize": true
						},
						"modes": {
							"grab": {
								"distance": 400,
								"line_linked": {
									"opacity": 1
								}
							},
							"bubble": {
								"distance": 400,
								"size": 40,
								"duration": 2,
								"opacity": 8,
								"speed": 3
							},
							"repulse": {
								"distance": 200,
								"duration": 0.4
							},
							"push": {
								"particles_nb": 4
							},
							"remove": {
								"particles_nb": 2
							}
						}
					},
					"retina_detect": false

				})
			}
		}

	}
</script>

<style>
	/* Your styles */
</style>
