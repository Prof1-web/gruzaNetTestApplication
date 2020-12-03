export default {
    state: {
        list: []
    },
    actions: {
        // get users list
        usersList(ctx, rolePath) {
            return new Promise(resolve => {
                let urlPath = "/users/list"
                if (rolePath) {
                    urlPath = urlPath + "?path=" + rolePath
                }
                ctx.dispatch('request', {method: "GET", path: urlPath})
                .then(r => {
                    if (r.status == 200) {
                        ctx.commit('setUsersList', r.content)
                    }
                    resolve()
                })
            })
        }
    },
    mutations: {
        setUsersList(state, value) {
            state.list = value
        }
    },
    getters: {
        usersList(state) {
            return state.list
        }
    }
}
