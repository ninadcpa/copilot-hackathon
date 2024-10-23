package com.example.okta_demo_v1.configuration;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;



@EnableWebSecurity
@Configuration
public class OktaOAuth2WebSecurityConfiguration {

    @Bean
    SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http.authorizeHttpRequests(
                        (req) -> req.requestMatchers("/api/whoami").authenticated()
                                .requestMatchers("/**").permitAll()
                )
                .oauth2ResourceServer((srv) -> srv.jwt(Customizer.withDefaults()))
                .cors(Customizer.withDefaults())
                .build();
    }
}