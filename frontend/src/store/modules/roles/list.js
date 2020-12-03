export default {
    state: {
        list: []
    },
    actions: {
        // get roles list
        rolesList(ctx) {
            return new Promise(resolve => {
                ctx.dispatch('request', {method: "GET", path: "/users/roles-list"})
                .then(r => {
                    if (r.status == 200) {
                        ctx.commit('setRolesList', r.content)
                    }
                    resolve()
                })
            })
        }
    },
    mutations: {
        setRolesList(state, value) {
            state.list = value
        }
    },
    getters: {
        rolesList(state) {
            return state.list
        }
    }
}
