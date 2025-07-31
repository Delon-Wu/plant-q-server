from rest_framework import serializers

class PlantImageSerializer(serializers.Serializer):
    image = serializers.ImageField(
        max_length=None,
        allow_empty_file=False,
        use_url=False,
        help_text="上传的植物图片，支持格式：png, jpg, jpeg, bmp，大小不超过4MB。"
    )

    def validate_image(self, value):
        """验证图片格式和大小"""
        # 允许的格式
        valid_extensions = ['png', 'jpg', 'jpeg', 'bmp']
        extension = value.name.split('.')[-1].lower()
        
        if extension not in valid_extensions:
            raise serializers.ValidationError(
                f"不支持的图片格式: {extension}. 请上传: {', '.join(valid_extensions)}"
            )
        
        # 最大大小 4MB (4 * 1024 * 1024 bytes)
        max_size = 4 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError(
                f"图片大小超过限制 ({value.size} bytes). 最大允许 {max_size} bytes"
            )
        return value