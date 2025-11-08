document.addEventListener('DOMContentLoaded', function() {
    // === 表单提交验证 ===
    const form = document.getElementById('poll-form');

    form.addEventListener('submit', function(e) {
        // 检查有效的选项数量（非空的选项）
        const optionInputs = document.querySelectorAll('.option-item input');
        let validCount = 0;

        optionInputs.forEach(input => {
            if (input.value.trim() !== '') {
                validCount++;
            }
        });

        // 要求至少2个有效选项
        if (validCount < 1) {
            e.preventDefault();
            alert('请至少添加1个有效的投票选项！');
            return false;
        }

        console.log('表单验证通过，正在提交...');
        console.log('有效选项数量:', validCount);
        return true;
    });

    // === 添加选项按钮功能 ===
    document.getElementById('add-option-btn').addEventListener('click', function() {
        // 获取模板内容
        const template = document.getElementById('option-template');

        // 克隆模板内容
        const newOption = template.content.cloneNode(true);
        const optionItem = newOption.querySelector('.option-item');
        const input = newOption.querySelector('input');
        const deleteBtn = newOption.querySelector('.delete-btn');

        // 删除按钮功能
        deleteBtn.addEventListener('click', function() {
            optionItem.remove();
            console.log('选项框已删除');
        });

        // 添加到容器
        document.getElementById('options-container').appendChild(newOption);

        // 自动聚焦到新添加的输入框
        input.focus();

        console.log('新选项已添加');
        //alert('创建成功！');
    });
});

document.getElementById('create-poll-btn').addEventListener('click', function() {
    console.log('创建投票按钮点击');
    alert('创建投票成功！');
});
