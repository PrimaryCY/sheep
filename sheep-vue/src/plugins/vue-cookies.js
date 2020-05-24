import Vue from 'vue'
import VueCookies from 'vue-cookies';
import CryptoJS from "crypto-js";

Vue.use(VueCookies)

let secure_key = 'sadkladlkadjasjldsajkld'

VueCookies.secure_set = function (keyName,value,expireTimes, path, domain, secure) {
	let data = {
		'data':value
	}
	data = JSON.stringify(data)
	let cipherText = CryptoJS.AES.encrypt(
		data,
		secure_key
	).toString();
	VueCookies.set(keyName, cipherText, expireTimes,path,domain,secure)
}

VueCookies.secure_get = function (keyName) {
	let cipherText = VueCookies.get(keyName)
	if(!cipherText){
		return
	}
	let bytes = CryptoJS.AES.decrypt(cipherText, secure_key);
	let originalText = bytes.toString(CryptoJS.enc.Utf8);
	originalText = JSON.parse(originalText)
	return originalText['data'];
}

export default VueCookies
