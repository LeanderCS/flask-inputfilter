#ifndef HELPER_H
#define HELPER_H

#include <vector>
#include <string>

inline std::vector<std::string> make_default_methods() {
    return {
        "GET",
        "POST",
        "PATCH",
        "PUT",
        "DELETE"
    };
}

#endif
