let re = {}

//邮箱正则校验
function email(){
	re._email = /^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/;
	return re._email
}
re.email = email()

//手机号正则校验
function phone() {
	re._phone = /^1[3456789]\d{9}$/
	return re._phone
}
re.phone=phone()

//特殊字符校验
function special_str() {
	re._special_str=/[`~!@#$^&*()=|{}':;',[\].<>/?~！@#￥……&*（）——|{}【】‘；：”“'。，、？]/
	return re._special_str
}
re.special_str=special_str()

export default re
