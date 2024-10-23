package com.example.okta_demo_v1.controller;

import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import org.springframework.web.bind.annotation.CrossOrigin;

@RestController
public class SampleController {

    @GetMapping("/api/hello")
    public String anon() {
        return "Anonymous access";
    }

    @GetMapping("/api/whoami")
    @CrossOrigin(origins = "http://example.com")
    public String whoami(Authentication authentication) {
        return authentication.getDetails().toString();
    }
}