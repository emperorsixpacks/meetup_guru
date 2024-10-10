use lettre::{Message, SmtpTransport};


const Email = Message::builder()
    .from("NoBody <nobody@domain.tld>".parse().unwrap())
    .reply_to("Yuin <yuin@domain.tld>".parse().unwrap())
    .to("Hei <hei@domain.tld>".parse().unwrap())
    .subject("Happy new year")
    .body("Be happy!")
    .unwrap();

// Open a local connection on port 25 and send the email
const mailer = SmtpTransport::unencrypted_localhost();
assert!(mailer.send(&email).is_ok());