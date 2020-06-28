import CryptoJS from "crypto-js";


let secure_key = 'sadkladlkadjasjldsajkld'
export default({app}, inject)=> {
  let Nuxt_cookies = app.$cookies
  Nuxt_cookies.secure_set = function (keyName, value, expireTimes, path, domain, secure) {
    let data = {
      'data': value
    }
    data = JSON.stringify(data)
    let cipherText = CryptoJS.AES.encrypt(
      data,
      secure_key
    ).toString();
    Nuxt_cookies.set(keyName, cipherText, expireTimes, path, domain, secure)
  }

  Nuxt_cookies.secure_get = function (keyName) {
    let cipherText = Nuxt_cookies.get(keyName)
    if (!cipherText) {
      return
    }
    try {
      let bytes = CryptoJS.AES.decrypt(cipherText, secure_key);
      let originalText = bytes.toString(CryptoJS.enc.Utf8);
      originalText = JSON.parse(originalText)
      return originalText['data'];
    }catch (e) {
      return cipherText
    }
  }
  inject('cookies', Nuxt_cookies)
  process.$cookies = Nuxt_cookies
}
