export function get_tree_first_node(tree) {
    console.log(tree)

    function fs(data) {
        console.log(data)
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
