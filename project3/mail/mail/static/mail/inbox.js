document.addEventListener("DOMContentLoaded", function () {
	// Use buttons to toggle between views
	document.querySelector("#inbox").addEventListener("click", () => load_mailbox("inbox"));
	document.querySelector("#sent").addEventListener("click", () => load_mailbox("sent"));
	document.querySelector("#archived").addEventListener("click", () => load_mailbox("archive"));
	document.querySelector("#compose").addEventListener("click", compose_email);

	// By default, load the inbox
	load_mailbox("inbox");
});

function compose_email() {
	// Show compose view and hide other views
	document.querySelector("#emails-view").style.display = "none";
	document.querySelector("#compose-view").style.display = "block";

	// Clear out composition fields
	document.querySelector("#compose-recipients").value = "";
	document.querySelector("#compose-subject").value = "";
	document.querySelector("#compose-body").value = "";

	document.querySelector("form").onsubmit = compose_submit;
}

// After click SUBMIT
function compose_submit() {
	// Get form values
	const compose_recipients = document.querySelector("#compose-recipients").value;
	const compose_subject = document.querySelector("#compose-subject").value;
	const compose_body = document.querySelector("#compose-body").value;

	// POST mail
	fetch("/emails", {
		method: "POST",
		body: JSON.stringify({
			recipients: compose_recipients,
			subject: compose_subject,
			body: compose_body
		})
	})
		.then(response => response.json())
		.then(result => {
			// Print result
			console.log(result);
			load_mailbox("sent", result);
		});
	return false;
}

function load_mailbox(mailbox, result) {
	// Show the mailbox and hide other views
	document.querySelector("#emails-view").style.display = "block";
	document.querySelector("#compose-view").style.display = "none";

	// Show the mailbox name
	document.querySelector("#emails-view").innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

	mailbox_view(mailbox, result);
}
// Load mailbox
function mailbox_view(mailbox, result) {
	// Get emails from db
	fetch(`/emails/${mailbox}`)
		.then(response => response.json())
		.then(emails => {
			// Print emails
			console.log(emails);
			// ... do something else with emails ...
			// Save emails_view div
			let emails_view = document.querySelector("#emails-view");

			// Check for any messages
			if (result !== undefined) {
				if (result.error !== undefined) {
					var message = result.error;
					const mess = document.createElement("div");
					mess.classList.add("alert", "alert-danger");
					mess.innerHTML = message;

					emails_view.insertBefore(mess, emails_view.firstChild);
				} else if (result.message !== undefined) {
					var message = result.message;
					const mess = document.createElement("div");
					mess.classList.add("alert", "alert-success");
					mess.innerHTML = message;

					emails_view.insertBefore(mess, emails_view.firstChild);
				}
			}

			// For each email construct div
			for (let i = 0; i < emails.length; i++) {
				// Main div
				const mail = document.createElement("div");
				mail.classList.add("row", "mail", "p-2", "mb-3");

				// Different bg for read/unread email
				if (emails[i].read == true) {
					mail.style.backgroundColor = "#e6e6e6";
				}

				let id = emails[i].id;

				// Add addEventListener to redirect to single email view
				mail.addEventListener("click", function () {
					read_change(id);
					view_email(id, mailbox);
				});

				// Creating child div's
				const sender = document.createElement("div");
				sender.innerHTML = `${emails[i]["sender"]}`;
				sender.classList.add("col-2", "sender");

				const subject = document.createElement("div");
				subject.innerHTML = `${emails[i]["subject"]}`;
				subject.classList.add("col-6", "subject");

				const timestamp = document.createElement("div");
				timestamp.innerHTML = `${emails[i]["timestamp"]}`;
				timestamp.classList.add("col-4", "text-right", "timestamp");

				const clear = document.createElement("div");
				clear.style.clear = "both";

				// Put it all together
				mail.append(sender);
				mail.append(subject);
				mail.append(timestamp);
				mail.append(clear);

				emails_view.append(mail);
			}
		});
}

// Single email view
function view_email(id, mailbox) {
	fetch(`/emails/${id}`)
		.then(response => response.json())
		.then(email => {
			// Print email
			console.log(email);
			// ... do something else with email ...

			// Get email_view and clear it
			let emails_view = document.querySelector("#emails-view");
			emails_view.innerHTML = "";

			// Create new div for all email content
			const mail = document.createElement("div");
			mail.classList.add("row", "mail_view", "justify-content-center");

			// Create new div for SENDER
			const from = document.createElement("div");
			from.classList.add("col-8", "from_view");
			from.innerHTML = `<strong>From:</strong> ${email["sender"]}`;

			// Create new div for TIMESTAMP
			const timestamp = document.createElement("div");
			timestamp.classList.add("col-4", "text-right", "timestamp_view");
			timestamp.innerHTML = `<strong>${email["timestamp"]}</strong>`;

			// Create new div for RECIPIENTS
			const recipients = document.createElement("div");
			recipients.classList.add("col-12", "recipients_view");
			recipients.innerHTML = `<strong>To:</strong> ${email["recipients"]}`;

			// Create new div for SUBJECT
			const subject = document.createElement("div");
			subject.classList.add("col-12", "subject_view");
			subject.innerHTML = `<strong>${email["subject"]}</strong><hr>`;

			// Create new div for BODY
			const body = document.createElement("div");
			body.classList.add("col-10", "body_view");
			body.innerHTML = `${email["body"]}`;

			// Put it all together
			mail.append(from);
			mail.append(timestamp);
			mail.append(recipients);
			mail.append(subject);
			mail.append(body);

			// Create new div for BUTTONS
			const buttons = document.createElement("div");
			buttons.classList.add("col-12", "buttons_view", "text-right", "mt-2");

			// Create new div for ARCHIVE if mailbox is NOT IN SENT
			if (mailbox != "sent") {
				const archive = document.createElement("button");
				archive.classList.add("btn", "btn-outline-success", "btn-sm", "mr-3");
				if (email["archived"] == true) {
					archive.innerHTML = `Unarchive`;
					archive.addEventListener("click", function () {
						archive_change(id, true);
					});
				} else if (email["archived"] == false) {
					archive.innerHTML = `Archive`;
					archive.addEventListener("click", function () {
						archive_change(id, false);
					});
				} else {
					archive.innerHTML = `ERROR`;
				}
				buttons.append(archive);
			}

			// Create new div for REPLY
			const reply = document.createElement("button");
			reply.classList.add("btn", "btn-outline-primary", "btn-sm");
			reply.innerHTML = `Reply`;
			reply.addEventListener("click", function () {
				reply_email(email);
			});

			// Put it all together
			buttons.append(reply);
			mail.append(buttons);

			emails_view.append(mail);
		});
}

// Move email to archive
function archive_change(id, archived_val) {
	fetch(`/emails/${id}`, {
		method: "PUT",
		body: JSON.stringify({
			archived: !archived_val
		})
	});

	// Create message
	if (archived_val) {
		var message = { message: "Email moved to inbox." };
	} else {
		var message = { message: "Email archived successfully." };
	}
	// To let refresh inbox
	setTimeout(function () {
		load_mailbox("inbox", message);
	}, 100);
	return false;
}

// Mark email as read
function read_change(id) {
	fetch(`/emails/${id}`, {
		method: "PUT",
		body: JSON.stringify({
			read: true
		})
	});
}

// Reply to email
function reply_email(email) {
	// Change visibility of views
	document.querySelector("#emails-view").style.display = "none";
	document.querySelector("#compose-view").style.display = "block";

	// Fill out form fields
	document.querySelector("#compose-recipients").value = email["sender"];

	if (email["subject"].slice(0, 3) == "Re:") {
		document.querySelector("#compose-subject").value = email["subject"];
	} else {
		document.querySelector("#compose-subject").value = `Re: ${email["subject"]}`;
	}

	document.querySelector("#compose-body").value = `On ${email["timestamp"]} ${email["sender"]} wrote:\n${email["body"]}\n`;

	document.querySelector("form").onsubmit = compose_submit;
}
