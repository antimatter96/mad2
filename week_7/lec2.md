Store
-> State
-> Mutations

SIngle shared object

- Tree strucutre to capture component nesting
- Normal Data Object

Components can still have local state

- Isolated / Protected form others

Getter methods

- Computed properties on shared state objects
- Avoiding obj1.obj2....

Access within COmponents

- `this.$store` available within all components

--

Mutations

- Commit a mutation
- No direct update

  - Call a method that updates
  - Commit this action -> can track and record

- MUST BE SYNC

Can playback in order
Reproduce steps

---

```
mutations: {
  increment: (state, x) {
    state.count += x;
  }
}
```

...
...

```
store.commit('icrement')
store.commit('icrement', 10)
store.commit('icrement', {
  'a': 'b',
})
```

Async Code can be added in actions

```
actions: {
  increment: ({ commit }) {
    commit('mutation_name')
  },
}

store.dispatch('increment')
```

eg

```js
actions: {
  increment: ({ commit, state }, products) {
    sometinh = state.card.saved;
    commit('mutation_name');

    httpCall_buySomething([products, somethoin],
      () => {
        commit('update sdgsg')
        commit('sucrss')
      }, () => {
        commit('failures', [prodycs, someh])
      }
    )
  },
}

```

```js
actions: {
  async A: ({ commit, state }, ...) {
   ...
   commiy
   ...
  },
  async B: ({ commit, state, dispatch }, ...) {
   await dispatch('A')
   ...
  },
}

```


Select the statements that hold true for the store in Vuex.

- ❌ There can be multiple stores for multiple components in an application.
Vue stores are reactive.
The states in a store should only be changed through committing mutations.
A state change should never be triggered using store getters.


--

Which of the following statement(s) is/are true about Vuex debugging support?

Vue DevTools allows time travel debugging, i.e., possible to retrace steps.
Vue DevTools lists all mutations requested, time of mutations, and which component requested mutation.
Vue DevTools allow us to record mutation.
