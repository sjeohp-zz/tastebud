# Be sure to restart your server when you modify this file.

# Your secret key is used for verifying the integrity of signed cookies.
# If you change this key, all old signed cookies will become invalid!

# Make sure the secret is at least 30 characters and all random,
# no regular words or you'll be exposed to dictionary attacks.
# You can use `rake secret` to generate a secure secret key.

# Make sure your secret_key_base is kept private
# if you're sharing your code publicly.
Tastebud::Application.config.secret_key_base = if Rails.env.development? or Rails.env.test?
	# 'ab44def5a1c973b8061df0c03dcfd73bef4e1394b529e5dd62cf22b93a8bf5c242bcd6bf45bcc513a30a2f96ed93cd64bac083652e01dea573bb3a956e2f0447'
	('x' * 30) # meets minimum requirement of 30 chars long
else
	ENV['SECRET_TOKEN']
end
