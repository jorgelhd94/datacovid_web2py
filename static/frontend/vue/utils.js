// ASSUMES Vue and Axios

utils = {};
// load components lazily: https://vuejs.org/v2/guide/components.html#Async-Components
utils.register_vue_component = function (name, src, onload) {
    Vue.component(name, function (resolve, reject) {
        axios.get(src).then(function (data) { resolve(onload(data)); });
    });
};
