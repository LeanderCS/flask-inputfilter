#ifndef HELPER_H
#define HELPER_H

#include <unordered_set>
#include <string>

inline std::unordered_set<std::string> make_default_methods_set() {
    return {
        "GET",
        "POST",
        "PATCH",
        "PUT",
        "DELETE"
    };
}

#endif
