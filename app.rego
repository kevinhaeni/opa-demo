package demo

default allow = false
 
hr_employees = ["charlie"]
administrators = ["charlie"]

allow {
    input.method = "GET" 
    input.path = ["employees"]
}

allow {
    input.method = "GET"
    input.path = ["employees", name]
    its_own_data
}

allow {
    input.method = "POST" 
    input.path = ["employees", user_name]
    its_own_data
    is_admin
}


# Helper to get the token payload.
token = {"payload": payload} {
  [header, payload, signature] := io.jwt.decode(input.user)
}

its_own_data { 
    input.path = ["employees", name]
    token.payload.user_name = name
}

is_HR {
    token.payload.user_name = hr_employees[_]
}

is_admin {
    token.payload.user_name = administrators[_]
}