package com.example.okta_demo_v1.controller;

import com.example.okta_demo_v1.service.ApiService;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.client.RestTemplate;
import org.springframework.beans.factory.annotation.Autowired;

@RestController
public class SampleController {


    @Autowired
    public ApiService apiService;


    @GetMapping("/api/hello")
    public String anon() {
        return "Anonymous access";
    }

    @GetMapping("/api/copilot/creds")
    @CrossOrigin(origins = "http://example.com")
    public String whoami(Authentication authentication) {


        return apiService.callApi();
//        return authentication.getDetails().toString();
    }
}
