import 'package:flutter/material.dart';
import '../../core/services/api_service.dart';

class PageScreen extends StatefulWidget {
  final String slug;
  const PageScreen({super.key, required this.slug});

  @override
  State<PageScreen> createState() => _PageScreenState();
}

class _PageScreenState extends State<PageScreen> {
  String? title;
  String? content;
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchPage();
  }

  void fetchPage() async {
    try {
      final data = await ApiService.get("/page/${widget.slug}");
      setState(() {
        title = data['title'];
        content = data['content'];
        loading = false;
      });
    } catch (_) {
      setState(() {
        title = "Page Not Found";
        content = "";
        loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(title ?? "")),
      body: loading
          ? const Center(child: CircularProgressIndicator())
          : SingleChildScrollView(
              padding: const EdgeInsets.all(16),
              child: Text(content ?? ""),
            ),
    );
  }
}

