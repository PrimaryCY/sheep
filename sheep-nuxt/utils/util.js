
export function get_tree_first_node(tree){
  console.log(tree)
  function fs (data) {
    console.log(data)
    for(let i of data){
      if(!i.child||!i.child.length){
        return i.id
      }else {
        return fs(i['child'])
      }
    }
  }
  return fs(tree)
}

export function guid() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
    var r = Math.random() * 16 | 0,
    v = c == 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

export function extname(filename){
  if(!filename||typeof filename!='string'){
    return ''
  }
  let a = filename.split('').reverse().join('');
  return a.substring(0,a.search(/\./)).split('').reverse().join('');
}


