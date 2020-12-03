import { createStore } from 'vuex'

// users
import usersList from './modules/users/list'

// roles
import rolesList from './modules/roles/list'


export default createStore({
    state: {
        // backend url
        backendUrl: "https://prof1-web.ru:5001",
        // backend api version
        apiVersion: '1'
    },
    actions: {
        // default request template, instead of axios
        request(ctx, data) {
			return new Promise((resolve) => {
				let url = ctx.state.backendUrl + '/api/v' + ctx.state.apiVersion + data.path
				let sendData = (data.sendData) ? JSON.stringify(data.sendData) : null
				let xhr = new XMLHttpRequest()
				xhr.open(data.method, url, true)
				xhr.send(sendData)
				xhr.onreadystatechange = function() {
					if (xhr.readyState != 4) return;

					let content
					try {
						content = JSON.parse(xhr.responseText)
					} catch {
						content = null
					}

                    // show modal window with error
					if (xhr.status == 500) {
						let errorData
						if (content) {
							errorData = {
								head: "Ошибка",
								text: content.detail
							}
						} else {
							errorData = {
								head: "Ошибка",
								text: "Внутренняя ошибка сервера"
							}
						}

						ctx.commit('showModalWindow', errorData)
					}
                    // return status & responseData
					resolve({status: xhr.status, content})
				}
			})
		}
    },
    getters: {
        backendUrl(state) {
            return state.backendUrl
        }
    },
    modules: {
        // users
        usersList,

        // roles
        rolesList
    }
})
