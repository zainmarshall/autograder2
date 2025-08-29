$props
On this page
$props
Fallback values
Renaming props
Rest props
Updating props
Type safety
$props.id()
The inputs to a component are referred to as props, which is short for properties. You pass props to components just like you pass attributes to elements:

App

<script lang="ts">
	import MyComponent from './MyComponent.svelte';
</script>

<MyComponent adjective="cool" />
On the other side, inside MyComponent.svelte, we can receive props with the $props rune...

MyComponent

<script lang="ts">
	let props = $props();
</script>

<p>this component is {props.adjective}</p>
...though more commonly, you’ll destructure your props:

MyComponent

<script lang="ts">
	let { adjective } = $props();
</script>

<p>this component is {adjective}</p>
Fallback values
Destructuring allows us to declare fallback values, which are used if the parent component does not set a given prop (or the value is undefined):


let { adjective = 'happy' } = $props();
Fallback values are not turned into reactive state proxies (see Updating props for more info)

Renaming props
We can also use the destructuring assignment to rename props, which is necessary if they’re invalid identifiers, or a JavaScript keyword like super:


let { super: trouper = 'lights are gonna find me' } = $props();
Rest props
Finally, we can use a rest property to get, well, the rest of the props:


let { a, b, c, ...others } = $props();
Updating props
References to a prop inside a component update when the prop itself updates — when count changes in App.svelte, it will also change inside Child.svelte. But the child component is able to temporarily override the prop value, which can be useful for unsaved ephemeral state (demo):

App

<script lang="ts">
	import Child from './Child.svelte';

	let count = $state(0);
</script>

<button onclick={() => (count += 1)}>
	clicks (parent): {count}
</button>

<Child {count} />
Child

<script lang="ts">
	let { count } = $props();
</script>

<button onclick={() => (count += 1)}>
	clicks (child): {count}
</button>
While you can temporarily reassign props, you should not mutate props unless they are bindable.

If the prop is a regular object, the mutation will have no effect (demo):

App

<script lang="ts">
	import Child from './Child.svelte';
</script>

<Child object={{ count: 0 }} />
Child

<script lang="ts">
	let { object } = $props();
</script>

<button onclick={() => {
	// has no effect
	object.count += 1
}}>
	clicks: {object.count}
</button>
If the prop is a reactive state proxy, however, then mutations will have an effect but you will see an ownership_invalid_mutation warning, because the component is mutating state that does not ‘belong’ to it (demo):

App

<script lang="ts">
	import Child from './Child.svelte';

	let object = $state({count: 0});
</script>

<Child {object} />
Child

<script lang="ts">
	let { object } = $props();
</script>

<button onclick={() => {
	// will cause the count below to update,
	// but with a warning. Don't mutate
	// objects you don't own!
	object.count += 1
}}>
	clicks: {object.count}
</button>
The fallback value of a prop not declared with $bindable is left untouched — it is not turned into a reactive state proxy — meaning mutations will not cause updates (demo)

Child

<script lang="ts">
	let { object = { count: 0 } } = $props();
</script>

<button onclick={() => {
	// has no effect if the fallback value is used
	object.count += 1
}}>
	clicks: {object.count}
</button>
In summary: don’t mutate props. Either use callback props to communicate changes, or — if parent and child should share the same object — use the $bindable rune.

Type safety
You can add type safety to your components by annotating your props, as you would with any other variable declaration. In TypeScript that might look like this...


<script lang="ts">
	let { adjective }: { adjective: string } = $props();
</script>
...while in JSDoc you can do this:


<script>
	/** @type {{ adjective: string }} */
	let { adjective } = $props();
</script>
You can, of course, separate the type declaration from the annotation:


<script lang="ts">
	interface Props {
		adjective: string;
	}

	let { adjective }: Props = $props();
</script>
Interfaces for native DOM elements are provided in the svelte/elements module (see Typing wrapper components)

Adding types is recommended, as it ensures that people using your component can easily discover which props they should provide.

$props.id()
This rune, added in version 5.20.0, generates an ID that is unique to the current component instance. When hydrating a server-rendered component, the value will be consistent between server and client.

This is useful for linking elements via attributes like for and aria-labelledby.


<script>
	const uid = $props.id();
</script>

<form>
	<label for="{uid}-firstname">First Name: </label>
	<input id="{uid}-firstname" type="text" />

	<label for="{uid}-lastname">Last Name: </label>
	<input id="{uid}-lastname" type="text" />
</form>
