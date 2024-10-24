package com.example.okta_demo_v1.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.Base64;

@Service
public class ApiService {

    @Autowired
    private OktaTokenService oktaTokenService;

    @Autowired
    private RestTemplate restTemplate;

    public String callApi() {
        String accessToken = oktaTokenService.getAccessToken();

        HttpHeaders headers = new HttpHeaders();
        headers.setBearerAuth(accessToken);
        headers.set("JWT-TOKEN", accessToken);

        String[] chunks = accessToken.split("\\.");

        Base64.Decoder decoder = Base64.getUrlDecoder();

        String header = new String(decoder.decode(chunks[0]));
        String payload = new String(decoder.decode(chunks[1]));


        HttpEntity<String> entity = new HttpEntity<>(headers);

        String reqPayload= "{\"userid\": \"user1\"}";

        RequestEntity<String> requestEntity = new RequestEntity<>(reqPayload, headers, HttpMethod.POST, java.net.URI.create("https://8jip41mb78.execute-api.us-west-2.amazonaws.com/v1/token"));

        ResponseEntity<String> responseEntity = restTemplate.exchange(requestEntity, String.class);

        return responseEntity.getBody();
    }
}
