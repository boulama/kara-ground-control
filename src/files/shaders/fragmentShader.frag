#version 330

in vec3 normalInterp;
in vec3 vertexPositionEye;

uniform vec3 lightPosition;
uniform vec3 lightIntensity;

out vec4 fragColor;

void main()
{
    vec3 n = normalize(normalInterp);
    vec3 l = normalize(lightPosition - vertexPositionEye);
    float lambertian = max(dot(l, n), 0.0);
    fragColor = vec4(lightIntensity * lambertian, 1.0);
}