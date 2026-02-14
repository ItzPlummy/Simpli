class Shaders:
    VERTEX_SHADER = """
        #version 150 core
    
        in vec2 position;
        in vec2 translation;
        in vec4 colors;
        in float zposition;
        in float rotation;
    
        out vec4 vertex_colors;
    
        uniform WindowBlock
        {
            mat4 projection;
            mat4 view;
        } window;
        uniform vec2 u_window_size;
        uniform vec2 u_camera_position;
        uniform float u_zoom;
    
        void main()
        {
            float theta = radians(rotation);
            float s = sin(theta);
            float c = cos(theta);
            vec2 rotated = vec2(
                position.x * c - position.y * s,
                position.x * s + position.y * c
            );
    
            vec2 world_position = translation + rotated;
    
            gl_Position = window.projection * window.view * vec4((world_position - u_camera_position) * u_zoom + (u_window_size * 0.5), zposition, 1.0);
            vertex_colors = colors;
        }
    """

    FRAGMENT_SHADER = """
        #version 150 core
    
        in vec4 vertex_colors;
    
        out vec4 final_color;
    
        void main()
        {
            final_color = vertex_colors;
            if (final_color.a < 0.01) discard;
        }
    """

    LAYOUT_VERTEX_SHADER = """
        #version 330 core
    
        in vec3 position;
        in vec4 colors;
        in vec3 tex_coords;
        in vec3 translation;
        in vec3 view_translation;
        in vec2 anchor;
        in float rotation;
        in float visible;
    
        out vec4 text_colors;
        out vec2 texture_coords;
        out vec4 vert_position;
    
        uniform WindowBlock
        {
            mat4 projection;
            mat4 view;
        } window;
        uniform vec3 u_window_size;
        uniform vec3 u_camera_position;
        uniform float u_zoom;
    
        void main()
        {
            vec3 local = position + vec3(anchor, 0.0) + view_translation;
    
            float t = radians(rotation);
            float s = sin(t);
            float c = cos(t);
    
            vec3 rotated = vec3(
                local.x * c - local.y * s,
                local.x * s + local.y * c,
                local.z
            );
    
            vec3 world_position = translation + rotated;
            vec3 screen = (world_position - u_camera_position) * u_zoom + u_window_size * 0.5;
    
            gl_Position = window.projection * window.view * vec4(screen, 1.0);
            vert_position = vec4(screen, 1.0);
    
            texture_coords = tex_coords.xy;
            text_colors = colors * visible;
        }
    """

    LAYOUT_FRAGMENT_SHADER = """
        #version 330 core
    
        in vec4 text_colors;
        in vec2 texture_coords;
        in vec4 vert_position;
    
        out vec4 final_colors;
    
        uniform sampler2D text;
        uniform bool scissor;
        uniform vec4 scissor_area;
    
        void main()
        {
            final_colors = texture(text, texture_coords) * text_colors;
    
            if (scissor == true) {
                if (vert_position.x < scissor_area[0]) discard;
                if (vert_position.y < scissor_area[1]) discard;
                if (vert_position.x > scissor_area[0] + scissor_area[2]) discard;
                if (vert_position.y > scissor_area[1] + scissor_area[3]) discard;
            }
        }
    """
