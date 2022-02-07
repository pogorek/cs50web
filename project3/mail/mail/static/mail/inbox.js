document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('form').onsubmit = compose_submit;

  // By default, load the inbox
  load_mailbox('inbox');
});

// After click SUBMIT
function compose_submit() {

  // Get form values
  const compose_recipients = document.querySelector('#compose-recipients').value;
  const compose_subject = document.querySelector('#compose-subject').value;
  const compose_body = document.querySelector('#compose-body').value;

  // POST mail
  fetch('/emails', {
    method: 'POST',
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
  });

}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  mailbox_view(mailbox);

}
// Load mailbox
function mailbox_view(mailbox) {

  // get emails from db
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);
      // ... do something else with emails ...
      // Save emails_view div
      let emails_view = document.querySelector('#emails-view');

      // For each email construct div
      for (let i = 0; i < emails.length; i++) {
        // Main div
        const mail = document.createElement('div');
        mail.classList.add('mail');
        // Different bg for read/unread email
        if (emails[i].read == true) {
          mail.style.backgroundColor = "#ddd";
        }
        let id = emails[i].id;
        // Add addEventListener to redirect to single email view
        mail.addEventListener('click', function() { read_change(id); view_email(id, mailbox); });
        
        // Creating child div's
        const sender = document.createElement('div');
        sender.innerHTML = `sender: ${emails[i]["sender"]}`;
        sender.classList.add('sender');

        const subject = document.createElement('div');
        subject.innerHTML = `SUBJECT: ${emails[i]["subject"]}`;
        subject.classList.add('subject');

        const timestamp = document.createElement('div');
        timestamp.innerHTML = `timestamp: ${emails[i]["timestamp"]}`;
        timestamp.classList.add('timestamp');

        const clear = document.createElement('div');
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
      let emails_view = document.querySelector('#emails-view');
      emails_view.innerHTML = '';

      // Create new div for ROW
      const mail = document.createElement('div');
      mail.classList.add('row', 'mail_view', 'justify-content-center');

      // Create new div for SENDER 
      const from = document.createElement('div');
      from.classList.add('col-8');
      from.innerHTML = `<strong>From:</strong> ${email["sender"]}`;

      // Create new div for TIMESTAMP 
      const timestamp = document.createElement('div');
      timestamp.classList.add('col-4', 'text-right');
      timestamp.innerHTML = `<strong>${email["timestamp"]}</strong>`;

      // Create new div for RECIPIENTS 
      const recipients = document.createElement('div');
      recipients.classList.add('col-12');
      recipients.innerHTML = `<strong>To:</strong> ${email["recipients"]}`;

      // Create new div for SUBJECT 
      const subject = document.createElement('div');
      subject.classList.add('col-12');
      subject.innerHTML = `<strong>${email["subject"]}</strong>`;

      // Create new div for BODY 
      const body = document.createElement('div');
      body.classList.add('col-8');
      body.innerHTML = `body: ${email["body"]}`;

      // Put it all together
      mail.append(from);
      mail.append(timestamp);
      mail.append(recipients);
      mail.append(subject);
      mail.append(body);

      // Create new div for ARCHIVE if mailbox is not SENT
      if (mailbox != 'sent') {
        const archive = document.createElement('button');
        archive.classList.add('btn', 'btn-primary');
        if (email["archived"] == true) {
          archive.innerHTML = `ARCHIVED YES: ${email["archived"]}`;
          archive.addEventListener('click', function() { archive_change(id, true); });
        }
        else if (email["archived"] == false) {
          archive.innerHTML = `ARCHIVED NO: ${email["archived"]}`;
          archive.addEventListener('click', function() { archive_change(id, false); });
        }
        else {
          archive.innerHTML = `ERROR`;
        }
        mail.append(archive);
      }

      const reply = document.createElement('button');
      reply.classList.add('btn', 'btn-primary');
      reply.innerHTML = `Reply`;
      reply.addEventListener('click', function() { reply_email(email); });

      mail.append(reply);

      emails_view.append(mail);
  });
}

// Move email to archive
function archive_change(id, archived_val) {
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: !archived_val
      })
    })
  // To let refresh inbox
  setTimeout(function() { load_mailbox('inbox'); }, 100)
}

// Mark as read mail
function read_change(id) {
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
        read: true
      })
    })

}

// Reply to email
function reply_email(email) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = email["sender"];

  if (email["subject"].slice(0, 3) == "Re:") {
    document.querySelector('#compose-subject').value = email["subject"];
  }
  else {
    document.querySelector('#compose-subject').value = `Re: ${email["subject"]}`;
  }
  
  //document.querySelector('#compose-subject').value = `>${email["subject"].slice(0, 2)}<`;

  document.querySelector('#compose-body').value = `On ${email["timestamp"]} ${email["sender"]} wrote:\n${email["body"]}\n`;
}