export default {
	name: "",
	render(createElement) {
		console.log('sadsadasd')
	return createElement('script', {attrs: {type: 'text/javascript', src: this.src}});
},
	props: {
		src: { type: String, required: true}
	}
}
