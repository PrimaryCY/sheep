export function dateFormat(fmt, date) {
    /* 时间字符串格式化
            let date = new Date()
            dateFormat("YYYY-mm-dd HH:MM", date)
            >>> 2019-06-06 19:45`
     */
    let ret
    const opt = {
        "Y+": date.getFullYear().toString(),        // 年
        "m+": (date.getMonth() + 1).toString(),     // 月
        "d+": date.getDate().toString(),            // 日
        "H+": date.getHours().toString(),           // 时
        "M+": date.getMinutes().toString(),         // 分
        "S+": date.getSeconds().toString()          // 秒
        // 有其他格式化字符需求可以继续添加，必须转化成字符串
    }
    for (let k in opt) {
        ret = new RegExp("(" + k + ")").exec(fmt)
        if (ret) {
            fmt = fmt.replace(ret[1], (ret[1].length == 1) ? (opt[k]) : (opt[k].padStart(ret[1].length, "0")))
        }

    }

    return fmt
}


export function get_tree_first_node(tree) {
    function fs(data) {
        for (let i of data) {
            if (!i.child || !i.child.length) {
                return i.id
            } else {
                return fs(i['child'])
            }
        }
    }

    return fs(tree)
}

export function guid() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = Math.random() * 16 | 0,
                v = c == 'x' ? r : (r & 0x3 | 0x8)
        return v.toString(16)
    })
}

export function extname(filename) {
    if (!filename || typeof filename != 'string') {
        return ''
    }
    let a = filename.split('').reverse().join('')
    return a.substring(0, a.search(/\./)).split('').reverse().join('')
}


export let pickerOptions = {
    shortcuts: [{
        text: '最近一周',
        onClick(picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
            picker.$emit('pick', [start, end])
        }
    }, {
        text: '最近一个月',
        onClick(picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
            picker.$emit('pick', [start, end])
        }
    }, {
        text: '最近三个月',
        onClick(picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
            picker.$emit('pick', [start, end])
        }
    }]
}
