document.addEventListener("DOMContentLoaded", function () {
	// Use buttons to toggle between views
	// document.querySelector("#inbox").addEventListener("click", () => load_mailbox("inbox"));

	// document.querySelector("#compose").addEventListener("click", compose_email);

	// By default, load the inbox
	// load_mailbox("inbox");
	// alert("OOOKKOO");
	// document.querySelector("form").onsubmit = compose_submit;
	document.getElementById("user_follow").addEventListener("click", user_following);
});

// After click SUBMIT
function compose_submit() {
	alert("NEW POST SUBMIT");
	// Get form values
	const new_post_textarea = document.querySelector("#new_post_textarea").value;

	// POST new_post
	fetch("/new_post", {
		method: "POST",
		body: JSON.stringify({
			new_post_textarea: new_post_textarea,
		}),
	});
	// .then(response => response.json())
	// .then(result => {
	// 	// Print result
	// 	console.log(result);
	// 	load_mailbox("sent", result);
	// });
	return false;
}

function user_following() {
	alert("FOLL");
}
